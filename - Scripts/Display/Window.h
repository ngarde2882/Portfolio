#include <Windows.h>

class Window {
    Window();
    Window(const Window&) = delete;
    Window& operator =(const Window&) = delete;
    ~Window();

    bool ProcessMessages();
private:
    HINSTANCE m_hInstance;
    HWND m_hWnd;
};
