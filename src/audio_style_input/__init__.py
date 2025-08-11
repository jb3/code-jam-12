import asyncio
from pathlib import Path

from nicegui import app, ui

media = Path("./static")
app.add_media_files("/media", media)

letters = [chr(i) for i in range(ord("A"), ord("Z") + 1)]


async def spin_continuous(
    rotation_container: list[int],
    spin_direction_container: list[int],
    spin_speed_container: list[int],
    record: ui.image,
) -> None:
    """Continuously rotate the record image based on spin direction and speed."""
    while True:
        rotation_container[0] += spin_direction_container[0] * spin_speed_container[0]
        record.style(f"transform: rotate({rotation_container[0]}deg);")
        await asyncio.sleep(0.05)


def create_intro_card() -> tuple[ui.card, ui.button]:
    """Create the intro card with title and start button."""
    intro_card = ui.card().classes("w-[100vw] h-[50vh] flex justify-center items-center bg-[#d18b2b]")
    with intro_card, ui.card().classes("no-shadow justify-center items-center"):
        ui.label("WPM Battle: DJ Edition").classes("text-[86px]")
        ui.label("Use an audio editor to test your typing skills").classes("text-[28px]")
        start_button = ui.button("Get started!", color="#ff9900")

    return intro_card, start_button


def create_main_content() -> tuple[ui.column, ui.image, ui.label, ui.row]:
    """Create the main content area with record image, letter label, and buttons inside the same card."""
    main_content = ui.column().classes("items-center gap-4 #2b87d1").style("display:none")
    with (
        main_content,
        ui.card().classes(
            "gap-8 w-[100vw] h-[50vh] flex flex-col justify-center items-center bg-[#2b87d1]",
        ),
    ):
        record = ui.image(
            "/media/images/record.png",
        ).style("width: 300px; transition: transform 0.05s linear;")
        label = ui.label("Current letter: A")
        buttons_row = ui.row().style("gap: 10px")
    return main_content, record, label, buttons_row


@ui.page("/audio_editor")
def audio_editor_page() -> None:  # noqa: C901 , PLR0915
    """Render the audio editor page with spinning record and letter spinner."""
    current_letter_index_container: list[int] = [0]
    rotation_container: list[int] = [0]
    normal_spin_speed = 5
    boosted_spin_speed = 10
    spin_speed_container: list[int] = [normal_spin_speed]
    spin_direction_container: list[int] = [1]

    timer_task: asyncio.Task | None = None
    spin_task: asyncio.Task | None = None

    main_track = (
        ui.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3")
        .props(remove="controls")
        .props("loop")
    )
    rewind_sound = ui.audio("/media/sounds/rewind.mp3").style("display:none")
    fast_forward_sound = ui.audio("/media/sounds/fast_forward.mp3").style("display:none")

    intro_card, start_button = create_intro_card()
    main_content, record, label, buttons_row = create_main_content()

    async def letter_spinner_task() -> None:
        while True:
            label.set_text(f"Current letter: {letters[current_letter_index_container[0]]}")
            current_letter_index_container[0] = (current_letter_index_container[0] + 1) % len(letters)
            await asyncio.sleep(0.5)

    def start_spinning(*, clockwise: bool = True) -> None:
        nonlocal spin_task
        spin_direction_container[0] = 1 if clockwise else -1
        if spin_task is None or spin_task.done():
            spin_task = asyncio.create_task(
                spin_continuous(
                    rotation_container,
                    spin_direction_container,
                    spin_speed_container,
                    record,
                ),
            )

    def stop_spinning() -> None:
        nonlocal spin_task
        if spin_task:
            spin_task.cancel()

    async def speed_boost(final_direction: int = 1) -> None:
        spin_speed_container[0] = boosted_spin_speed
        await asyncio.sleep(1)
        spin_speed_container[0] = normal_spin_speed
        spin_direction_container[0] = final_direction

    def on_play() -> None:
        nonlocal timer_task
        if timer_task is None or timer_task.done():
            timer_task = asyncio.create_task(letter_spinner_task())
        start_spinning(clockwise=True)

    def on_pause() -> None:
        nonlocal timer_task
        if timer_task:
            timer_task.cancel()
        stop_spinning()

    def play_rewind_sound() -> None:
        rewind_sound.play()

    def play_fast_forward_sound() -> None:
        fast_forward_sound.play()

    def forward_3() -> None:
        current_letter_index_container[0] = (current_letter_index_container[0] + 3) % len(letters)
        play_fast_forward_sound()
        start_spinning(clockwise=True)
        task = asyncio.create_task(speed_boost(final_direction=1))
        _ = task

    def rewind_3() -> None:
        current_letter_index_container[0] = (current_letter_index_container[0] - 3) % len(letters)
        play_rewind_sound()
        start_spinning(clockwise=False)
        task = asyncio.create_task(speed_boost(final_direction=1))
        _ = task

    handlers = {
        "on_play": on_play,
        "on_pause": on_pause,
        "rewind_3": rewind_3,
        "forward_3": forward_3,
    }

    with buttons_row:
        ui.button("Play", color="#d18b2b", on_click=lambda: [main_track.play(), handlers["on_play"]()])
        ui.button("Pause", color="#d18b2b", on_click=lambda: [main_track.pause(), handlers["on_pause"]()])
        ui.button("Rewind 3 Seconds", color="#d18b2b", on_click=handlers["rewind_3"])
        ui.button("Forward 3 Seconds", color="#d18b2b", on_click=handlers["forward_3"])
        ui.button(
            "Select Letter",
            color="green",
            on_click=lambda: ui.notify(
                f"You selected: {letters[current_letter_index_container[0] - 1]}",
            ),
        )

    def start_audio_editor() -> None:
        intro_card.style("display:none")
        main_content.style("display:flex")

    start_button.on("click", start_audio_editor)
