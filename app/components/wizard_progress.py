import reflex as rx
from app.states.kyc_state import KYCState


def step_indicator(index: int, label: str) -> rx.Component:
    """Renders a single step in the progress bar."""
    is_active = KYCState.current_step == index
    is_completed = KYCState.current_step > index
    circle_base = "flex items-center justify-center w-8 h-8 sm:w-10 sm:h-10 rounded-full text-sm font-semibold transition-all duration-300 z-10 border-2"
    circle_style = rx.cond(
        is_completed,
        "bg-indigo-600 border-indigo-600 text-white",
        rx.cond(
            is_active,
            "bg-white border-indigo-600 text-indigo-600 shadow-[0_0_0_4px_rgba(79,70,229,0.2)]",
            "bg-white border-gray-300 text-gray-400",
        ),
    )
    label_style = rx.cond(
        is_active,
        "text-indigo-600 font-semibold",
        rx.cond(is_completed, "text-indigo-600", "text-gray-400"),
    )
    return rx.el.div(
        rx.el.div(
            rx.cond(
                is_completed,
                rx.icon("check", class_name="w-5 h-5"),
                rx.el.span(f"{index + 1}"),
            ),
            class_name=f"{circle_base} {circle_style}",
        ),
        rx.el.span(
            label,
            class_name=f"mt-2 text-xs sm:text-sm transition-colors duration-300 {label_style}",
        ),
        class_name="flex flex-col items-center relative",
    )


def wizard_progress() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name="absolute top-4 sm:top-5 left-0 w-full h-0.5 bg-gray-200 -z-0"
        ),
        rx.el.div(
            style={"width": KYCState.progress_percentage},
            class_name="absolute top-4 sm:top-5 left-0 h-0.5 bg-indigo-600 -z-0 transition-all duration-500 ease-in-out",
        ),
        rx.el.div(
            rx.foreach(
                KYCState.steps,
                lambda step, i: rx.el.div(
                    step_indicator(i, step), class_name="flex-1 flex justify-center"
                ),
            ),
            class_name="flex justify-between w-full relative z-10",
        ),
        class_name="relative w-full max-w-3xl mx-auto px-4 mb-12",
    )