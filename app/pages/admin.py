import reflex as rx
from app.states.kyc_state import KYCState
from app.states.admin_state import AdminState
from app.components.admin_login_page import admin_login_page


def status_pill(status: str) -> rx.Component:
    return rx.el.span(
        status,
        class_name=rx.match(
            status,
            (
                "Verified",
                "px-3 py-1 rounded-full bg-green-100 text-green-800 text-xs font-bold",
            ),
            (
                "Pending Review",
                "px-3 py-1 rounded-full bg-yellow-100 text-yellow-800 text-xs font-bold",
            ),
            (
                "In Review",
                "px-3 py-1 rounded-full bg-blue-100 text-blue-800 text-xs font-bold",
            ),
            (
                "Rejected",
                "px-3 py-1 rounded-full bg-red-100 text-red-800 text-xs font-bold",
            ),
            "px-3 py-1 rounded-full bg-gray-100 text-gray-800 text-xs font-bold",
        ),
    )


def submission_row(sub: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            sub["id"],
            class_name="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900",
        ),
        rx.el.td(
            sub["name"], class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-700"
        ),
        rx.el.td(
            sub["email"], class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
        ),
        rx.el.td(
            sub["submitted_date"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(status_pill(sub["status"]), class_name="px-6 py-4 whitespace-nowrap"),
        rx.el.td(
            rx.el.button(
                "View",
                on_click=lambda: KYCState.view_submission(sub["id"]),
                class_name="text-indigo-600 hover:text-indigo-900 font-medium text-sm",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
        class_name="hover:bg-gray-50 transition-colors",
    )


def submission_detail_modal() -> rx.Component:
    sub = KYCState.selected_submission
    return rx.cond(
        KYCState.admin_view_submission_id != "",
        rx.el.div(
            rx.el.div(
                class_name="fixed inset-0 bg-gray-900/50 backdrop-blur-sm transition-opacity z-40",
                on_click=KYCState.close_submission_view,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Submission Details",
                            class_name="text-xl font-bold text-gray-900",
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="w-5 h-5"),
                            on_click=KYCState.close_submission_view,
                            class_name="text-gray-400 hover:text-gray-600",
                        ),
                        class_name="flex justify-between items-center mb-6",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                "Applicant",
                                class_name="text-xs text-gray-500 uppercase font-semibold",
                            ),
                            rx.el.p(
                                sub["name"],
                                class_name="text-base font-medium text-gray-900",
                            ),
                            rx.el.p(sub["email"], class_name="text-sm text-gray-500"),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Documents",
                                class_name="text-xs text-gray-500 uppercase font-semibold mb-2",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.image(
                                        src=rx.get_upload_url(
                                            sub["documents"]["front"]
                                        ),
                                        class_name="w-full h-32 object-cover rounded-lg bg-gray-100",
                                    ),
                                    rx.el.p(
                                        "Front",
                                        class_name="text-xs text-center mt-1 text-gray-500",
                                    ),
                                ),
                                rx.el.div(
                                    rx.image(
                                        src=rx.get_upload_url(sub["documents"]["back"]),
                                        class_name="w-full h-32 object-cover rounded-lg bg-gray-100",
                                    ),
                                    rx.el.p(
                                        "Back",
                                        class_name="text-xs text-center mt-1 text-gray-500",
                                    ),
                                ),
                                rx.el.div(
                                    rx.image(
                                        src=rx.get_upload_url(
                                            sub["documents"]["selfie"]
                                        ),
                                        class_name="w-full h-32 object-cover rounded-lg bg-gray-100",
                                    ),
                                    rx.el.p(
                                        "Selfie",
                                        class_name="text-xs text-center mt-1 text-gray-500",
                                    ),
                                ),
                                class_name="grid grid-cols-3 gap-4",
                            ),
                            class_name="mb-6",
                        ),
                        rx.cond(
                            sub["status"] == "Pending Review",
                            rx.el.div(
                                rx.el.div(
                                    rx.el.button(
                                        "Approve Application",
                                        on_click=lambda: KYCState.update_submission_status(
                                            sub["id"], "Verified"
                                        ),
                                        class_name="w-full py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium mb-3",
                                    ),
                                    class_name="mb-4 border-b border-gray-200 pb-4",
                                ),
                                rx.el.div(
                                    rx.el.label(
                                        "Rejection Reason",
                                        class_name="block text-sm font-medium text-gray-700 mb-1",
                                    ),
                                    rx.el.textarea(
                                        placeholder="Enter reason for rejection...",
                                        on_change=KYCState.set_rejection_reason_input,
                                        class_name="w-full p-2 border border-gray-300 rounded-lg mb-2 text-sm",
                                        default_value=KYCState.rejection_reason_input,
                                    ),
                                    rx.el.button(
                                        "Reject Application",
                                        on_click=lambda: KYCState.update_submission_status(
                                            sub["id"], "Rejected"
                                        ),
                                        class_name="w-full py-2 bg-red-50 text-red-600 border border-red-200 rounded-lg hover:bg-red-100 font-medium",
                                    ),
                                ),
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Status:", class_name="text-sm text-gray-500 mr-2"
                                ),
                                status_pill(sub["status"]),
                                rx.cond(
                                    sub["status"] == "Rejected",
                                    rx.el.p(
                                        f"Reason: {sub['rejection_reason']}",
                                        class_name="text-sm text-red-600 mt-2 italic",
                                    ),
                                ),
                                class_name="flex flex-col",
                            ),
                        ),
                        class_name="flex flex-col",
                    ),
                    class_name="bg-white w-full max-w-2xl mx-4 rounded-2xl shadow-2xl p-6 overflow-y-auto max-h-[90vh] z-50 relative animate-scale-in",
                ),
                class_name="fixed inset-0 flex items-center justify-center z-50 pointer-events-none",
                style={"pointer-events": "auto"},
            ),
        ),
    )


def admin_dashboard_content() -> rx.Component:
    return rx.el.div(
        submission_detail_modal(),
        rx.el.nav(
            rx.el.div(
                rx.el.div(
                    rx.icon("shield-check", class_name="w-8 h-8 text-indigo-600"),
                    rx.el.span(
                        "SecureKYC Admin",
                        class_name="ml-2 text-xl font-bold text-gray-900",
                    ),
                    class_name="flex items-center",
                ),
                rx.el.div(
                    rx.el.a(
                        "Back to Home",
                        href="/",
                        class_name="text-sm font-medium text-gray-500 hover:text-indigo-600 mr-4",
                    ),
                    rx.el.button(
                        "Sign Out",
                        on_click=AdminState.admin_logout,
                        class_name="text-sm font-medium text-gray-500 hover:text-red-600",
                    ),
                    class_name="flex items-center",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between",
            ),
            class_name="bg-white border-b border-gray-100",
        ),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "KYC Submissions", class_name="text-2xl font-bold text-gray-900"
                    ),
                    rx.el.div(
                        rx.foreach(
                            ["All", "Pending Review", "Verified", "Rejected"],
                            lambda s: rx.el.button(
                                s,
                                on_click=lambda: KYCState.set_admin_filter(s),
                                class_name=rx.cond(
                                    KYCState.admin_filter_status == s,
                                    "px-4 py-2 rounded-lg bg-indigo-600 text-white font-medium text-sm transition-colors",
                                    "px-4 py-2 rounded-lg bg-white text-gray-600 hover:bg-gray-50 font-medium text-sm transition-colors",
                                ),
                            ),
                        ),
                        class_name="flex gap-2",
                    ),
                    class_name="flex flex-col sm:flex-row justify-between items-center mb-8 gap-4",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "ID",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Applicant Name",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Email",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Date",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Status",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Actions",
                                    class_name="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                class_name="bg-gray-50",
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(KYCState.filtered_submissions, submission_row),
                            class_name="bg-white divide-y divide-gray-200",
                        ),
                        class_name="min-w-full divide-y divide-gray-200",
                    ),
                    class_name="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden",
                ),
                class_name="max-w-7xl mx-auto px-4 py-8",
            ),
            class_name="flex-1 bg-gray-50 min-h-[calc(100vh-80px)]",
        ),
        class_name="min-h-screen font-['Inter']",
    )


def admin_page() -> rx.Component:
    return rx.cond(
        AdminState.is_admin_authenticated, admin_dashboard_content(), admin_login_page()
    )