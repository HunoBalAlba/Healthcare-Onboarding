import reflex as rx
from app.states.kyc_state import KYCState


def info_row(label: str, value: str) -> rx.Component:
    return rx.el.div(
        rx.el.span(label, class_name="text-sm text-gray-500 font-medium"),
        rx.el.span(value, class_name="text-sm text-gray-900 font-semibold text-right"),
        class_name="flex justify-between items-center py-2 border-b border-gray-50 last:border-0",
    )


def doc_preview_thumb(label: str, filename: str) -> rx.Component:
    return rx.el.div(
        rx.el.p(label, class_name="text-xs text-gray-500 mb-2 font-medium"),
        rx.cond(
            filename != "",
            rx.image(
                src=rx.get_upload_url(filename),
                class_name="w-full h-24 object-cover rounded-lg border border-gray-200",
                alt=label,
            ),
            rx.el.div(
                "No Image",
                class_name="w-full h-24 bg-gray-100 rounded-lg flex items-center justify-center text-xs text-gray-400",
            ),
        ),
        class_name="flex flex-col",
    )


def review_submit_step() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Review Application", class_name="text-2xl font-bold text-gray-900 mb-2"
            ),
            rx.el.p(
                "Please review your information carefully before submitting.",
                class_name="text-gray-500 text-sm mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Personal Details",
                        class_name="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-4",
                    ),
                    rx.el.div(
                        info_row(
                            "Full Name",
                            f"{KYCState.form_data['first_name']} {KYCState.form_data['last_name']}",
                        ),
                        info_row("Email", KYCState.form_data["email"]),
                        info_row("Phone", KYCState.form_data["phone"]),
                        info_row("Date of Birth", KYCState.form_data["dob"]),
                        info_row(
                            "Address",
                            f"{KYCState.form_data['address']}, {KYCState.form_data['city']}",
                        ),
                        info_row(
                            "Region",
                            f"{KYCState.form_data['state']}, {KYCState.form_data['zip_code']}",
                        ),
                        info_row("Country", KYCState.form_data["country"]),
                        class_name="bg-gray-50/50 rounded-xl p-5 mb-8",
                    ),
                    class_name="w-full",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Documents",
                        class_name="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                "Document Type:", class_name="text-sm text-gray-500"
                            ),
                            rx.el.span(
                                KYCState.document_type,
                                class_name="text-sm font-semibold text-gray-900 ml-2",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            doc_preview_thumb("Front Side", KYCState.id_front),
                            doc_preview_thumb("Back Side", KYCState.id_back),
                            doc_preview_thumb("Selfie", KYCState.selfie_photo),
                            class_name="grid grid-cols-3 gap-4",
                        ),
                        class_name="bg-gray-50/50 rounded-xl p-5 mb-8",
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        rx.el.input(
                            type="checkbox",
                            checked=KYCState.terms_accepted,
                            on_change=KYCState.toggle_terms,
                            class_name="w-5 h-5 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500 mt-0.5",
                        ),
                        rx.el.div(
                            rx.el.span(
                                "I confirm that the information provided is accurate and I agree to the ",
                                class_name="text-gray-700",
                            ),
                            rx.el.span(
                                "Terms and Conditions",
                                class_name="text-indigo-600 font-semibold cursor-pointer hover:underline",
                            ),
                            rx.el.span(" and ", class_name="text-gray-700"),
                            rx.el.span(
                                "Privacy Policy",
                                class_name="text-indigo-600 font-semibold cursor-pointer hover:underline",
                            ),
                            class_name="ml-3 text-sm",
                        ),
                        class_name="flex items-start cursor-pointer p-4 border border-gray-200 rounded-xl hover:bg-gray-50 transition-colors",
                    ),
                    class_name="mb-6",
                ),
            ),
            class_name="animate-fade-in w-full",
        ),
        class_name="w-full",
    )