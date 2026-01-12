import reflex as rx
from app.states.kyc_state import KYCState
from app.components.wizard_progress import wizard_progress
from app.components.personal_info_form import personal_info_form
from app.components.document_upload_form import document_upload_form
from app.components.selfie_capture_form import selfie_capture_form
from app.components.review_submit_step import review_submit_step
from app.pages.dashboard import dashboard_page
from app.pages.admin import admin_page


def success_modal() -> rx.Component:
    return rx.cond(
        KYCState.is_submission_success,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "circle_check_big",
                        class_name="w-20 h-20 text-green-500 mb-4 animate-bounce",
                    ),
                    rx.el.h3(
                        "Application Submitted!",
                        class_name="text-2xl font-bold text-gray-900 mb-2",
                    ),
                    rx.el.p(
                        "We have received your KYC documents and will review them shortly.",
                        class_name="text-gray-500 text-center mb-8",
                    ),
                    rx.el.button(
                        "Continue to Dashboard",
                        on_click=KYCState.continue_to_dashboard,
                        class_name="w-full py-3 bg-indigo-600 text-white rounded-xl font-semibold hover:bg-indigo-700 transition-colors shadow-lg shadow-indigo-200",
                    ),
                    class_name="bg-white p-8 rounded-3xl shadow-2xl flex flex-col items-center max-w-sm w-full mx-4 transform transition-all scale-100",
                ),
                class_name="fixed inset-0 flex items-center justify-center z-[60]",
            ),
            rx.el.div(
                class_name="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 transition-opacity"
            ),
            class_name="relative z-[100]",
        ),
    )


def step_content() -> rx.Component:
    """Determines which component to render based on current step."""
    return rx.match(
        KYCState.current_step,
        (0, personal_info_form()),
        (1, document_upload_form()),
        (2, selfie_capture_form()),
        (3, review_submit_step()),
        rx.el.div("Unknown Step"),
    )


def navigation_buttons() -> rx.Component:
    return rx.el.div(
        rx.cond(
            KYCState.current_step > 0,
            rx.el.button(
                "Back",
                on_click=KYCState.prev_step,
                class_name="px-6 py-3 rounded-xl text-gray-600 font-semibold hover:bg-gray-100 transition-colors duration-200 flex items-center gap-2",
            ),
            rx.el.div(),
        ),
        rx.el.button(
            rx.cond(KYCState.current_step == 3, "Submit Application", "Next Step"),
            rx.icon("arrow-right", class_name="w-4 h-4 ml-2"),
            on_click=KYCState.next_step,
            disabled=rx.cond(
                KYCState.current_step == 3, ~KYCState.terms_accepted, False
            ),
            class_name=rx.cond(
                (KYCState.current_step == 3) & ~KYCState.terms_accepted,
                "px-8 py-3 rounded-xl bg-gray-300 text-gray-500 font-semibold cursor-not-allowed flex items-center",
                "px-8 py-3 rounded-xl bg-indigo-600 text-white font-semibold hover:bg-indigo-700 shadow-lg shadow-indigo-200 transition-all duration-200 flex items-center transform active:scale-95",
            ),
        ),
        class_name="flex justify-between items-center mt-10 pt-6 border-t border-gray-100",
    )


def index() -> rx.Component:
    return rx.el.div(
        success_modal(),
        rx.el.nav(
            rx.el.div(
                rx.el.div(
                    rx.icon("shield-check", class_name="w-8 h-8 text-indigo-600"),
                    rx.el.span(
                        "SecureKYC", class_name="ml-2 text-xl font-bold text-gray-900"
                    ),
                    class_name="flex items-center",
                ),
                rx.el.div(
                    rx.el.a(
                        "Dashboard",
                        href="/dashboard",
                        class_name="text-sm font-medium text-gray-500 hover:text-indigo-600 cursor-pointer transition-colors mr-4",
                    ),
                    rx.el.a(
                        "Admin",
                        href="/admin",
                        class_name="text-sm font-medium text-gray-500 hover:text-indigo-600 cursor-pointer transition-colors",
                    ),
                    class_name="hidden sm:flex",
                ),
                class_name="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between",
            ),
            class_name="bg-white border-b border-gray-100 sticky top-0 z-50 bg-opacity-90 backdrop-blur-md",
        ),
        rx.el.main(
            rx.el.div(
                wizard_progress(),
                rx.el.div(
                    step_content(),
                    navigation_buttons(),
                    class_name="bg-white rounded-2xl shadow-xl shadow-gray-200/50 border border-gray-100 p-6 sm:p-10 md:p-12 transition-all duration-500",
                ),
                rx.el.p(
                    rx.icon("lock", class_name="w-3 h-3 mr-1 inline"),
                    "Your information is encrypted and securely stored according to GDPR and local banking regulations.",
                    class_name="text-center text-xs text-gray-400 mt-8 flex items-center justify-center",
                ),
                class_name="max-w-3xl mx-auto px-4 py-12",
            ),
            class_name="flex-1",
        ),
        class_name="min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50/50 font-['Inter']",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        )
    ],
)
app.add_page(index, route="/")
app.add_page(dashboard_page, route="/dashboard")
app.add_page(admin_page, route="/admin")