# Лабораторная работа №1
## Паттерн «Одиночка» (Singleton): Менеджер окон

## Предметная область

Паттерн **«Одиночка»** широко применяется в разработке десктопных и мобильных приложений для управления интерфейсными компонентами. Один из примеров – работа менеджера окон (Window Manager).

**Менеджер окон** – это компонент приложения, который отвечает за создание, отображение, активацию и закрытие окон. Он контролирует, чтобы для каждого типа окна в любой момент времени существовал не более одного экземпляра.

## Описание проблемы

В приложении с графическим интерфейсом пользователь может многократно нажимать на кнопки, открывающие одни и те же окна (например, кнопка «Настройки» в меню).

Если каждое нажатие будет создавать новый экземпляр окна:

1. **На экране появится множество одинаковых окон**, накладывающихся друг на друга;
2. **Пользователь запутается**, какое окно активное, а какое можно закрыть;
3. **Данные в разных экземплярах одного окна могут рассинхронизироваться** (например, пользователь изменил настройку в одном окне «Настройки», а в другом оно осталось старым).

## Решение проблемы

Использование **паттерна «Одиночка»** для классов окон.

Паттерн гарантирует, что:

1. Для каждого типа окна существует **не более одного экземпляра** в памяти приложения;
2. При повторном запросе на открытие окна возвращается **ссылка на уже созданный объект**;
3. Если окно было закрыто, при следующем запросе создаётся **новый экземпляр**.

##Реализация идеи без Singleton.

namespace WindowManagerApp.Models
{
    public class Window
    {
        public Guid Id { get; set; }
        public string Title { get; set; } = string.Empty;
        public DateTime CreatedAt { get; set; }
    }
}

using Microsoft.AspNetCore.Mvc;
using WindowManagerApp.Models;

namespace WindowManagerApp.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class WindowController : ControllerBase
    {
        private static List<Window> _windows = new();


        [HttpPost("open")]
    public ActionResult<Window> OpenWindow()
    {
        var existingWindow = _windows.FirstOrDefault(w => w.Title == "Настройки");

        if (existingWindow != null)
        {
            return Ok(existingWindow);
        }

        var window = new Window
        {
            Id = Guid.NewGuid(),
            Title = "Настройки",
            CreatedAt = DateTime.Now
        };

        _windows.Add(window);
        return Ok(window);
    }

        [HttpGet]
        public ActionResult<List<Window>> GetWindows()
        {
            return Ok(_windows);
        }

        [HttpDelete("{id}")]
        public IActionResult CloseWindow(Guid id)
        {
            var window = _windows.FirstOrDefault(w => w.Id == id);
            if (window == null)
                return NotFound();

            _windows.Remove(window);
            return NoContent();
        }
    }
}


##Реализация идеи с Singleton.
<img width="352" height="432" alt="Диаграмма без названия drawio (1)" src="https://github.com/user-attachments/assets/7ed5433a-d862-4e73-9ffc-6a852484a588" />

namespace WindowManagerSingleton.Models
{
    public class Window
    {
        public Guid Id { get; set; }
        public string Title { get; set; } = string.Empty;
        public DateTime CreatedAt { get; set; }
    }
}

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
