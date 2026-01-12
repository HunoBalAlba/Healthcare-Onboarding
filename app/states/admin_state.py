import reflex as rx


class AdminState(rx.State):
    admin_username: str = "admin"
    admin_password: str = "admin"
    is_admin_authenticated: bool = False
    admin_login_error: str = ""
    is_loading: bool = False

    @rx.event
    def set_admin_username(self, value: str):
        self.admin_username = value
        self.admin_login_error = ""

    @rx.event
    def set_admin_password(self, value: str):
        self.admin_password = value
        self.admin_login_error = ""

    @rx.event
    async def admin_login(self):
        self.is_loading = True
        yield
        import asyncio

        await asyncio.sleep(1)
        if self.admin_username == "admin" and self.admin_password == "admin":
            self.is_admin_authenticated = True
            self.admin_login_error = ""
            self.admin_username = ""
            self.admin_password = ""
        else:
            self.is_admin_authenticated = False
            self.admin_login_error = "Invalid username or password"
        self.is_loading = False

    @rx.event
    def admin_logout(self):
        self.is_admin_authenticated = False
        return rx.redirect("/")