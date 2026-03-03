using WindowManagerSingleton.Models;

namespace WindowManagerSingleton.Services
{
    public class WindowManager
    {
        private static WindowManager? _instance;

        private List<Window> _windows;

        private WindowManager()
        {
            _windows = new List<Window>();
        }

        public static WindowManager GetInstanceSingleton()
        {
            if (_instance == null)
            {
                _instance = new WindowManager();
            }

            return _instance;
        }
        public Window OpenWindow()
        {
            var existing = _windows.FirstOrDefault(w => w.Title == "Настройки");

            if (existing != null)
                return existing;

            var window = new Window
            {
                Id = Guid.NewGuid(),
                Title = "Настройки",
                CreatedAt = DateTime.Now
            };

            _windows.Add(window);
            return window;
        }

        public List<Window> GetWindows()
        {
            return _windows;
        }

        public bool CloseWindow(Guid id)
        {
            var window = _windows.FirstOrDefault(w => w.Id == id);
            if (window == null)
                return false;

            _windows.Remove(window);
            return true;
        }
    }
}