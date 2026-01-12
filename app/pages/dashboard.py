import reflex as rx
from app.states.kyc_state import KYCState


def status_badge(status: str) -> rx.Component:
    return rx.el.span(
        status,
        class_name=rx.match(
            status,
            (
                "Verified",
                "px-4 py-1.5 rounded-full bg-green-100 text-green-800 text-sm font-bold shadow-sm",
            ),
            (
                "Pending Review",
                "px-4 py-1.5 rounded-full bg-yellow-100 text-yellow-800 text-sm font-bold shadow-sm",
            ),
            (
                "In Review",
                "px-4 py-1.5 rounded-full bg-blue-100 text-blue-800 text-sm font-bold shadow-sm",
            ),
            (
                "Rejected",
                "px-4 py-1.5 rounded-full bg-red-100 text-red-800 text-sm font-bold shadow-sm",
            ),
            "px-4 py-1.5 rounded-full bg-gray-100 text-gray-800 text-sm font-bold shadow-sm",
        ),
    )


def timeline_item(
    title: str, date: str, status: str, is_last: bool = False
) -> rx.Component:
    active = True
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                class_name="absolute top-0 bottom-0 left-4 w-0.5 bg-gray-200",
                style=rx.cond(is_last, {"display": "none"}, {}),
            ),
            rx.el.div(
                rx.icon("check", class_name="w-4 h-4 text-white"),
                class_name="relative z-10 w-8 h-8 flex items-center justify-center rounded-full bg-indigo-600 shadow-sm border-2 border-white",
            ),
            class_name="relative mr-6",
        ),
        rx.el.div(
            rx.el.h4(title, class_name="text-base font-semibold text-gray-900"),
            rx.el.p(date, class_name="text-sm text-gray-500"),
            rx.el.p(status, class_name="text-sm text-gray-600 mt-1"),
            class_name="pb-8",
        ),
        class_name="flex",
    )


def dashboard_page() -> rx.Component:
    return rx.el.div(
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
                        "Admin Panel",
                        href="/admin",
                        class_name="text-sm font-medium text-gray-500 hover:text-indigo-600 mr-4",
                    ),
                    rx.el.button(
                        "Sign Out",
                        class_name="text-sm font-medium text-gray-500 hover:text-red-600",
                    ),
                    class_name="flex items-center",
                ),
                class_name="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between",
            ),
            class_name="bg-white border-b border-gray-100 sticky top-0 z-50",
        ),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h1(
                            "Verification Status",
                            class_name="text-2xl font-bold text-gray-900",
                        ),
                        status_badge(KYCState.submission_status),
                        class_name="flex items-center gap-4 mb-2",
                    ),
                    rx.el.p(
                        f"Application ID: {rx.cond(KYCState.submissions.length() > 0, KYCState.submissions[0]['id'], 'N/A')}",
                        class_name="text-gray-500 text-sm",
                    ),
                    class_name="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "Timeline",
                            class_name="text-lg font-bold text-gray-900 mb-6",
                        ),
                        rx.el.div(
                            timeline_item(
                                "Application Submitted",
                                KYCState.submission_date,
                                "Your application has been received.",
                            ),
                            timeline_item(
                                "Under Review",
                                "",
                                "Our team is currently reviewing your documents.",
                                is_last=True,
                            ),
                            class_name="pl-2",
                        ),
                        class_name="bg-white rounded-2xl shadow-sm border border-gray-100 p-8",
                    ),
                    rx.el.div(
                        rx.el.h2(
                            "Submitted Documents",
                            class_name="text-lg font-bold text-gray-900 mb-6",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.icon(
                                    "file-text",
                                    class_name="w-8 h-8 text-indigo-600 mb-3",
                                ),
                                rx.el.p(
                                    "Identity Document",
                                    class_name="font-semibold text-gray-900",
                                ),
                                rx.el.p(
                                    KYCState.document_type,
                                    class_name="text-sm text-gray-500",
                                ),
                                class_name="p-4 rounded-xl bg-gray-50 border border-gray-100 flex flex-col items-center text-center",
                            ),
                            rx.el.div(
                                rx.icon(
                                    "camera", class_name="w-8 h-8 text-indigo-600 mb-3"
                                ),
                                rx.el.p(
                                    "Biometric Photo",
                                    class_name="font-semibold text-gray-900",
                                ),
                                rx.el.p(
                                    "Selfie Uploaded",
                                    class_name="text-sm text-gray-500",
                                ),
                                class_name="p-4 rounded-xl bg-gray-50 border border-gray-100 flex flex-col items-center text-center",
                            ),
                            class_name="grid grid-cols-1 sm:grid-cols-2 gap-4",
                        ),
                        class_name="bg-white rounded-2xl shadow-sm border border-gray-100 p-8",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-8",
                ),
                class_name="max-w-5xl mx-auto px-4 py-8",
            ),
            class_name="flex-1 bg-gray-50 min-h-[calc(100vh-80px)]",
        ),
        class_name="min-h-screen font-['Inter']",
    )