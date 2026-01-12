import reflex as rx
from app.states.kyc_state import KYCState


def uploaded_file_preview(filename: str, field_name: str) -> rx.Component:
    """Component to display the uploaded file preview."""
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=rx.get_upload_url(filename),
                class_name="w-full h-48 object-cover rounded-t-lg opacity-90",
                alt="Document Preview",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("file-check", class_name="w-5 h-5 text-green-600 mr-2"),
                    rx.el.span(
                        filename,
                        class_name="text-sm text-gray-700 font-medium truncate flex-1",
                    ),
                    class_name="flex items-center w-full overflow-hidden",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="w-4 h-4"),
                    "Remove",
                    on_click=lambda: KYCState.remove_file(field_name),
                    class_name="ml-2 text-xs text-red-600 hover:text-red-700 font-semibold flex items-center gap-1 hover:bg-red-50 px-2 py-1 rounded transition-colors",
                ),
                class_name="p-3 bg-white border-t border-gray-200 rounded-b-lg flex items-center justify-between",
            ),
            class_name="w-full rounded-lg border border-gray-200 shadow-sm overflow-hidden bg-white",
        ),
        class_name="w-full animate-fade-in",
    )


def upload_zone(
    label: str,
    upload_id: str,
    current_file: str,
    field_key: str,
    upload_handler: rx.event.EventType,
    is_loading: bool,
) -> rx.Component:
    """Reusable upload zone component."""
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700 mb-2"),
        rx.cond(
            is_loading,
            rx.el.div(
                rx.spinner(size="3", class_name="text-indigo-600 mb-3"),
                rx.el.p(
                    "Uploading...", class_name="text-sm text-indigo-600 font-medium"
                ),
                class_name="flex flex-col items-center justify-center h-48 border-2 border-dashed border-indigo-200 rounded-xl bg-indigo-50/30 animate-pulse",
            ),
            rx.cond(
                current_file != "",
                uploaded_file_preview(current_file, field_key),
                rx.el.div(
                    rx.upload.root(
                        rx.el.div(
                            rx.icon(
                                "cloud-upload",
                                class_name="w-10 h-10 text-indigo-400 mb-3",
                            ),
                            rx.el.p(
                                "Drag and drop your file here",
                                class_name="text-sm text-gray-700 font-medium",
                            ),
                            rx.el.p(
                                "or click to select",
                                class_name="text-xs text-gray-400 mt-1",
                            ),
                            rx.el.p(
                                "Supports: JPG, PNG",
                                class_name="text-xs text-gray-400 mt-4 bg-gray-100 px-2 py-1 rounded",
                            ),
                            class_name="flex flex-col items-center justify-center py-8 px-4 w-full h-full",
                        ),
                        id=upload_id,
                        accept={"image/png": [], "image/jpeg": [], "image/jpg": []},
                        max_files=1,
                        on_drop=upload_handler(rx.upload_files(upload_id=upload_id)),
                        class_name="border-2 border-dashed border-gray-300 rounded-xl hover:bg-indigo-50/50 hover:border-indigo-300 transition-all cursor-pointer w-full bg-gray-50",
                    ),
                    rx.cond(
                        KYCState.errors.contains(field_key),
                        rx.el.p(
                            KYCState.errors[field_key],
                            class_name="mt-2 text-xs text-red-600 font-medium animate-pulse",
                        ),
                    ),
                    class_name="flex flex-col",
                ),
            ),
        ),
        class_name="flex flex-col h-full",
    )


def document_upload_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Document Verification",
                class_name="text-2xl font-bold text-gray-900 mb-2",
            ),
            rx.el.p(
                "Select your document type and upload clear images of both sides.",
                class_name="text-gray-500 text-sm mb-8",
            ),
            rx.el.div(
                rx.el.label(
                    "Document Type",
                    class_name="block text-sm font-medium text-gray-700 mb-2",
                ),
                rx.el.select(
                    rx.foreach(
                        KYCState.document_types, lambda x: rx.el.option(x, value=x)
                    ),
                    value=KYCState.document_type,
                    on_change=KYCState.set_document_type,
                    class_name="w-full px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-indigo-200 focus:border-indigo-500 outline-none transition-all bg-white text-gray-900 mb-8 cursor-pointer",
                ),
                class_name="w-full max-w-md",
            ),
            rx.el.div(
                upload_zone(
                    "Front of Document",
                    "front_upload",
                    KYCState.id_front,
                    "id_front",
                    KYCState.handle_front_upload,
                    KYCState.is_uploading_front,
                ),
                upload_zone(
                    "Back of Document",
                    "back_upload",
                    KYCState.id_back,
                    "id_back",
                    KYCState.handle_back_upload,
                    KYCState.is_uploading_back,
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
            ),
            class_name="animate-fade-in",
        ),
        class_name="w-full",
    )