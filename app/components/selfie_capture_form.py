import reflex as rx
from app.states.kyc_state import KYCState


def selfie_capture_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Identity Verification",
                class_name="text-2xl font-bold text-gray-900 mb-2",
            ),
            rx.el.p(
                "Please provide a photo of yourself to match with your document.",
                class_name="text-gray-500 text-sm mb-8",
            ),
            rx.el.div(
                rx.cond(
                    KYCState.is_uploading_selfie,
                    rx.el.div(
                        rx.spinner(
                            size="3", class_name="text-indigo-600 mb-4 w-12 h-12"
                        ),
                        rx.el.h3(
                            "Uploading your selfie...",
                            class_name="text-lg font-semibold text-gray-900",
                        ),
                        rx.el.p(
                            "This may take a few moments",
                            class_name="text-gray-500 text-sm",
                        ),
                        class_name="flex flex-col items-center justify-center py-12",
                    ),
                    rx.cond(
                        KYCState.selfie_photo != "",
                        rx.el.div(
                            rx.el.div(
                                rx.image(
                                    src=rx.get_upload_url(KYCState.selfie_photo),
                                    class_name="w-full h-full object-cover",
                                    alt="Selfie Preview",
                                ),
                                class_name="w-64 h-64 rounded-full border-4 border-indigo-100 shadow-xl overflow-hidden mb-6 mx-auto relative",
                            ),
                            rx.el.button(
                                rx.icon("refresh-cw", class_name="w-4 h-4 mr-2"),
                                "Retake Photo",
                                on_click=lambda: KYCState.remove_file("selfie_photo"),
                                class_name="mx-auto flex items-center px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors shadow-sm",
                            ),
                            class_name="flex flex-col items-center",
                        ),
                        rx.el.div(
                            rx.upload.root(
                                rx.el.div(
                                    rx.el.div(
                                        rx.icon(
                                            "camera", class_name="w-12 h-12 text-white"
                                        ),
                                        class_name="w-24 h-24 bg-indigo-500 rounded-full flex items-center justify-center shadow-lg shadow-indigo-200 mb-6 group-hover:scale-110 transition-transform duration-300",
                                    ),
                                    rx.el.h3(
                                        "Upload a Selfie",
                                        class_name="text-lg font-semibold text-gray-900 mb-2",
                                    ),
                                    rx.el.p(
                                        "Make sure your face is clearly visible and well-lit.",
                                        class_name="text-gray-500 text-sm max-w-xs",
                                    ),
                                    class_name="flex flex-col items-center text-center p-8",
                                ),
                                id="selfie_upload",
                                accept={
                                    "image/png": [],
                                    "image/jpeg": [],
                                    "image/jpg": [],
                                },
                                max_files=1,
                                on_drop=KYCState.handle_selfie_upload(
                                    rx.upload_files(upload_id="selfie_upload")
                                ),
                                class_name="border-2 border-dashed border-indigo-200 rounded-2xl bg-indigo-50/30 hover:bg-indigo-50 hover:border-indigo-400 transition-all cursor-pointer w-full max-w-md mx-auto group",
                            ),
                            rx.cond(
                                KYCState.errors.contains("selfie_photo"),
                                rx.el.p(
                                    KYCState.errors["selfie_photo"],
                                    class_name="mt-4 text-sm text-red-600 font-medium text-center animate-pulse",
                                ),
                            ),
                            class_name="flex flex-col items-center w-full",
                        ),
                    ),
                ),
                class_name="flex justify-center w-full py-8",
            ),
            class_name="animate-fade-in",
        ),
        class_name="w-full",
    )