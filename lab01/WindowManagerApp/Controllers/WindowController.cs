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
        // Проверяем, существует ли уже окно "Настройки"
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