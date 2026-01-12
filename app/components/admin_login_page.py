import reflex as rx
from app.states.admin_state import AdminState


def admin_login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "shield-check", class_name="w-8 h-8 text-indigo-600"
                            ),
                            class_name="w-16 h-16 bg-indigo-50 rounded-2xl flex items-center justify-center mb-6 mx-auto",
                        ),
                        rx.el.h2(
                            "Admin Access",
                            class_name="text-2xl font-bold text-gray-900 text-center tracking-tight mb-2",
                        ),
                        rx.el.p(
                            "Please enter your credentials to continue",
                            class_name="text-gray-500 text-center text-sm font-medium mb-8",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Username",
                            class_name="block text-xs font-semibold text-gray-700 uppercase tracking-wider mb-2 ml-1",
                        ),
                        rx.el.input(
                            placeholder="admin",
                            on_change=AdminState.set_admin_username,
                            class_name="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all duration-200 bg-gray-50 focus:bg-white text-gray-900 placeholder-gray-400 font-medium",
                            default_value=AdminState.admin_username,
                        ),
                        class_name="mb-5",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Password",
                            class_name="block text-xs font-semibold text-gray-700 uppercase tracking-wider mb-2 ml-1",
                        ),
                        rx.el.input(
                            type="password",
                            placeholder="••••••••",
                            on_change=AdminState.set_admin_password,
                            class_name="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all duration-200 bg-gray-50 focus:bg-white text-gray-900 placeholder-gray-400 font-medium",
                            default_value=AdminState.admin_password,
                        ),
                        class_name="mb-8",
                    ),
                    rx.cond(
                        AdminState.admin_login_error != "",
                        rx.el.div(
                            rx.icon(
                                "circle-alert", class_name="w-4 h-4 mr-2 flex-shrink-0"
                            ),
                            rx.el.span(
                                AdminState.admin_login_error,
                                class_name="text-sm font-medium",
                            ),
                            class_name="mb-6 p-3 bg-red-50 text-red-600 rounded-xl flex items-center animate-shake",
                        ),
                    ),
                    rx.el.button(
                        rx.cond(
                            AdminState.is_loading,
                            rx.el.div(
                                rx.spinner(size="2", class_name="text-white mr-2"),
                                "Authenticating...",
                                class_name="flex items-center justify-center",
                            ),
                            "Sign In",
                        ),
                        on_click=AdminState.admin_login,
                        disabled=AdminState.is_loading,
                        class_name="w-full py-3.5 bg-indigo-600 text-white rounded-xl font-semibold hover:bg-indigo-700 active:scale-[0.98] transition-all duration-200 shadow-lg shadow-indigo-600/20 disabled:opacity-70 disabled:cursor-not-allowed disabled:transform-none",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.icon("info", class_name="w-4 h-4 text-indigo-500 mr-2"),
                            rx.el.span(
                                "Demo Access:", class_name="text-indigo-600 mr-1"
                            ),
                            rx.el.span(
                                "admin / admin", class_name="font-bold text-indigo-800"
                            ),
                            class_name="inline-flex items-center px-5 py-2.5 rounded-full bg-indigo-50 border border-indigo-100 text-sm shadow-sm transition-transform hover:scale-105 cursor-default",
                        ),
                        class_name="mt-8 pt-6 border-t border-gray-100 flex justify-center",
                    ),
                    class_name="bg-white p-8 sm:p-12 rounded-[2rem] shadow-xl shadow-gray-200/50 border border-white w-full max-w-md relative overflow-hidden",
                ),
                rx.el.div(
                    class_name="absolute -top-24 -left-24 w-64 h-64 bg-indigo-100 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob"
                ),
                rx.el.div(
                    class_name="absolute -bottom-24 -right-24 w-64 h-64 bg-purple-100 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-2000"
                ),
                class_name="relative flex flex-col items-center justify-center min-h-screen px-4 z-10",
            ),
            class_name="absolute inset-0 z-10",
        ),
        class_name="relative min-h-screen bg-slate-50 font-['Inter'] overflow-hidden",
    )