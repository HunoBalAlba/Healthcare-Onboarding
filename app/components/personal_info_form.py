import reflex as rx
from app.states.kyc_state import KYCState


def form_field(
    label: str,
    placeholder: str,
    field_key: str,
    type: str = "text",
    col_span: str = "col-span-1",
) -> rx.Component:
    """Reusable form field component with error handling."""
    error_message = KYCState.errors[field_key]
    has_error = KYCState.errors.contains(field_key)
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700 mb-1"),
        rx.el.input(
            type=type,
            placeholder=placeholder,
            on_change=lambda val: KYCState.set_form_field(field_key, val),
            class_name=rx.cond(
                has_error,
                "w-full px-4 py-2.5 rounded-lg border border-red-300 focus:ring-2 focus:ring-red-200 focus:border-red-500 outline-none transition-all bg-red-50 text-gray-900 placeholder-red-300",
                "w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-200 focus:border-indigo-500 outline-none transition-all bg-white text-gray-900 placeholder-gray-400",
            ),
            default_value=KYCState.form_data[field_key],
        ),
        rx.cond(
            has_error,
            rx.el.p(
                error_message, class_name="mt-1 text-xs text-red-600 animate-fade-in"
            ),
        ),
        class_name=col_span,
    )


def personal_info_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Personal Information",
                class_name="text-2xl font-bold text-gray-900 mb-2",
            ),
            rx.el.p(
                "Please fill in your details exactly as they appear on your official identification documents.",
                class_name="text-gray-500 text-sm mb-8",
            ),
            rx.el.div(
                form_field("First Name", "e.g. John", "first_name"),
                form_field("Last Name", "e.g. Doe", "last_name"),
                form_field(
                    "Email Address",
                    "john@example.com",
                    "email",
                    type="email",
                    col_span="col-span-2 sm:col-span-1",
                ),
                form_field(
                    "Phone Number",
                    "+1 (555) 000-0000",
                    "phone",
                    type="tel",
                    col_span="col-span-2 sm:col-span-1",
                ),
                form_field(
                    "Date of Birth", "", "dob", type="date", col_span="col-span-2"
                ),
                rx.el.div(
                    rx.el.h3(
                        "Address Details",
                        class_name="text-sm font-semibold text-gray-900 uppercase tracking-wider mt-4 mb-2",
                    ),
                    class_name="col-span-2",
                ),
                form_field(
                    "Street Address", "123 Main St", "address", col_span="col-span-2"
                ),
                form_field("City", "New York", "city"),
                form_field("State / Province", "NY", "state"),
                form_field("Zip / Postal Code", "10001", "zip_code"),
                form_field("Country", "United States", "country"),
                class_name="grid grid-cols-2 gap-x-4 gap-y-6",
            ),
            class_name="animate-fade-in",
        ),
        class_name="w-full",
    )