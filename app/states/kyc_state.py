import reflex as rx
import re
import random
import string
from typing import TypedDict
from datetime import datetime


class Submission(TypedDict):
    id: str
    name: str
    email: str
    status: str
    submitted_date: str
    documents: dict[str, str]
    rejection_reason: str


class KYCState(rx.State):
    current_step: int = 0
    steps: list[str] = ["Personal Info", "Documents", "Verification", "Review"]
    form_data: dict[str, str] = {
        "first_name": "",
        "last_name": "",
        "email": "",
        "phone": "",
        "dob": "",
        "address": "",
        "city": "",
        "state": "",
        "zip_code": "",
        "country": "",
    }
    errors: dict[str, str] = {}
    document_type: str = "Passport"
    document_types: list[str] = [
        "Passport",
        "Driver's License",
        "National ID Card",
        "Residence Permit",
    ]
    id_front: str = ""
    id_back: str = ""
    selfie_photo: str = ""
    is_uploading_front: bool = False
    is_uploading_back: bool = False
    is_uploading_selfie: bool = False
    is_submission_success: bool = False
    terms_accepted: bool = False
    submission_status: str = "Not Started"
    submission_date: str = ""
    admin_filter_status: str = "All"
    admin_view_submission_id: str = ""
    rejection_reason_input: str = ""
    submissions: list[Submission] = []

    @rx.event
    def toggle_terms(self):
        self.terms_accepted = not self.terms_accepted

    @rx.event
    def set_document_type(self, value: str):
        self.document_type = value

    async def _handle_upload(self, files: list[rx.UploadFile], target_field: str):
        """Helper to handle file uploads securely."""
        upload_dir = rx.get_upload_dir()
        upload_dir.mkdir(parents=True, exist_ok=True)
        for file in files:
            upload_data = await file.read()
            unique_prefix = "".join(
                random.choices(string.ascii_letters + string.digits, k=10)
            )
            filename = f"{unique_prefix}_{file.name}"
            outfile = upload_dir / filename
            with outfile.open("wb") as f:
                f.write(upload_data)
            if target_field == "id_front":
                self.id_front = filename
                if "id_front" in self.errors:
                    self.errors.pop("id_front")
            elif target_field == "id_back":
                self.id_back = filename
                if "id_back" in self.errors:
                    self.errors.pop("id_back")
            elif target_field == "selfie_photo":
                self.selfie_photo = filename
                if "selfie_photo" in self.errors:
                    self.errors.pop("selfie_photo")

    @rx.event
    async def handle_front_upload(self, files: list[rx.UploadFile]):
        self.is_uploading_front = True
        yield
        await self._handle_upload(files, "id_front")
        self.is_uploading_front = False

    @rx.event
    async def handle_back_upload(self, files: list[rx.UploadFile]):
        self.is_uploading_back = True
        yield
        await self._handle_upload(files, "id_back")
        self.is_uploading_back = False

    @rx.event
    async def handle_selfie_upload(self, files: list[rx.UploadFile]):
        self.is_uploading_selfie = True
        yield
        await self._handle_upload(files, "selfie_photo")
        self.is_uploading_selfie = False

    @rx.event
    def remove_file(self, field: str):
        """Clear a specific file field."""
        if field == "id_front":
            self.id_front = ""
        elif field == "id_back":
            self.id_back = ""
        elif field == "selfie_photo":
            self.selfie_photo = ""

    @rx.event
    def set_form_field(self, field: str, value: str):
        """Update a specific field in the form data."""
        self.form_data[field] = value
        if field in self.errors:
            self.errors.pop(field)

    @rx.event
    def validate_personal_info(self) -> bool:
        """Validate step 1 fields."""
        new_errors = {}
        required_fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "dob",
            "address",
            "city",
            "state",
            "zip_code",
            "country",
        ]
        for field in required_fields:
            if not self.form_data.get(field):
                new_errors[field] = "This field is required"
        email = self.form_data.get("email", "")
        if email and (not re.match("[^@]+@[^@]+\\.[^@]+", email)):
            new_errors["email"] = "Invalid email format"
        self.errors = new_errors
        return len(new_errors) == 0

    @rx.event
    def validate_documents(self) -> bool:
        """Validate step 2: Documents."""
        new_errors = {}
        if not self.id_front:
            new_errors["id_front"] = "Front of document is required"
        if not self.id_back:
            new_errors["id_back"] = "Back of document is required"
        self.errors.update(new_errors)
        if self.id_front and "id_front" in self.errors:
            self.errors.pop("id_front")
        if self.id_back and "id_back" in self.errors:
            self.errors.pop("id_back")
        return len(new_errors) == 0

    @rx.event
    def validate_selfie(self) -> bool:
        """Validate step 3: Selfie."""
        if not self.selfie_photo:
            self.errors["selfie_photo"] = "Selfie photo is required"
            return False
        if "selfie_photo" in self.errors:
            self.errors.pop("selfie_photo")
        return True

    @rx.event
    def submit_application(self):
        """Submit the application and save to state."""
        if not self.terms_accepted:
            return rx.toast("Please accept the Terms and Conditions.")
        submission_id = f"SUB-{random.randint(2000, 9999)}"
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        new_submission: Submission = {
            "id": submission_id,
            "name": f"{self.form_data['first_name']} {self.form_data['last_name']}",
            "email": self.form_data["email"],
            "status": "Pending Review",
            "submitted_date": now,
            "documents": {
                "type": self.document_type,
                "front": self.id_front,
                "back": self.id_back,
                "selfie": self.selfie_photo,
            },
            "rejection_reason": "",
        }
        self.submissions.insert(0, new_submission)
        self.submission_status = "Pending Review"
        self.submission_date = now
        self.is_submission_success = True

    @rx.event
    def continue_to_dashboard(self):
        self.is_submission_success = False
        self.current_step = 0
        return rx.redirect("/dashboard")

    @rx.event
    def next_step(self):
        """Proceed to the next step if validation passes."""
        if self.current_step == 0:
            if self.validate_personal_info():
                self.current_step += 1
        elif self.current_step == 1:
            if self.validate_documents():
                self.current_step += 1
        elif self.current_step == 2:
            if self.validate_selfie():
                self.current_step += 1
        elif self.current_step == 3:
            self.submit_application()

    @rx.event
    def prev_step(self):
        """Go back to the previous step."""
        if self.current_step > 0:
            self.current_step -= 1

    @rx.var
    def progress_percentage(self) -> str:
        """Calculate progress percentage for the progress bar."""
        return f"{self.current_step / (len(self.steps) - 1) * 100}%"

    @rx.event
    def set_admin_filter(self, status: str):
        self.admin_filter_status = status

    @rx.event
    def view_submission(self, sub_id: str):
        self.admin_view_submission_id = sub_id
        self.rejection_reason_input = ""

    @rx.event
    def close_submission_view(self):
        self.admin_view_submission_id = ""
        self.rejection_reason_input = ""

    @rx.event
    def set_rejection_reason_input(self, value: str):
        self.rejection_reason_input = value

    @rx.event
    def update_submission_status(self, sub_id: str, new_status: str):
        for sub in self.submissions:
            if sub["id"] == sub_id:
                sub["status"] = new_status
                if new_status == "Rejected":
                    sub["rejection_reason"] = self.rejection_reason_input
                elif new_status == "Verified":
                    sub["rejection_reason"] = ""
                if sub["email"] == self.form_data["email"]:
                    self.submission_status = new_status
                break
        self.admin_view_submission_id = ""
        self.rejection_reason_input = ""
        return rx.toast(f"Submission {sub_id} updated to {new_status}")

    @rx.var
    def filtered_submissions(self) -> list[Submission]:
        if self.admin_filter_status == "All":
            return self.submissions
        return [s for s in self.submissions if s["status"] == self.admin_filter_status]

    @rx.var
    def selected_submission(self) -> Submission:
        default_sub: Submission = {
            "id": "",
            "name": "",
            "email": "",
            "status": "",
            "submitted_date": "",
            "documents": {"type": "", "front": "", "back": "", "selfie": ""},
            "rejection_reason": "",
        }
        if not self.admin_view_submission_id:
            return default_sub
        for sub in self.submissions:
            if sub["id"] == self.admin_view_submission_id:
                return sub
        return default_sub