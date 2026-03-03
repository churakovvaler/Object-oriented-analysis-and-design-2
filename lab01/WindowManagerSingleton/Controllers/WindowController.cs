using Microsoft.AspNetCore.Mvc;
using WindowManagerSingleton.Models;
using WindowManagerSingleton.Services;

namespace WindowManagerSingleton.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class WindowController : ControllerBase
    {
        private readonly WindowManager _manager;

        public WindowController()
        {
            _manager = WindowManager.GetInstanceSingleton();
        }

        [HttpPost("open")]
        public ActionResult<Window> OpenWindow()
        {
            return Ok(_manager.OpenWindow());
        }

        [HttpGet]
        public ActionResult<List<Window>> GetWindows()
        {
            return Ok(_manager.GetWindows());
        }

        [HttpDelete("{id}")]
        public IActionResult CloseWindow(Guid id)
        {
            var result = _manager.CloseWindow(id);

            if (!result)
                return NotFound();

            return NoContent();
        }
    }
}