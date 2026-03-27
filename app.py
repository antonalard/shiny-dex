import flet as ft
import requests


RELEASED_URL = "https://pogoapi.net/api/v1/released_pokemon.json"
SHINY_URL = "https://pogoapi.net/api/v1/shiny_pokemon.json"


def main(page: ft.Page):
    page.title = "Shinydex"
    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#000000"
    page.theme_mode = ft.ThemeMode.DARK

    all_pokemon_db = {}
    shiny_lookup_db = {}

    results_list = ft.Column(spacing=18)

    results_container = ft.Container(
        content=results_list,
        padding=ft.padding.symmetric(horizontal=20, vertical=20),
        visible=False,
    )

    def make_method_badge(emoji, text_value):
        return ft.Container(
            content=ft.Text(
                f"{emoji} {text_value}",
                color="white",
                size=11,
                weight=ft.FontWeight.BOLD,
            ),
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
            bgcolor="#000000",
            border_radius=18,
            border=ft.border.all(1, "#2a2a2a"),
        )

    def make_no_shiny_badge():
        return ft.Container(
            content=ft.Text(
                "❌ Finns ej som shiny",
                color="#ffcccc",
                size=11,
                weight=ft.FontWeight.BOLD,
            ),
            padding=ft.padding.symmetric(horizontal=14, vertical=9),
            bgcolor="#000000",
            border_radius=18,
            border=ft.border.all(1, "#4a1d1d"),
        )

    def build_image_label(text, color):
        return ft.Text(
            text,
            size=11,
            color=color,
            text_align=ft.TextAlign.CENTER,
        )

    def build_divider():
        return ft.Container(
            height=1,
            bgcolor="#000000",
            border_radius=10,
        )

    def build_pokemon_card(p_id, p_info, shiny_status):
        name = p_info.get("name", "Okänd")
        shiny_exists = shiny_status is not None

        normal_img_url = (
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/"
            f"sprites/pokemon/other/home/{p_id}.png"
        )

        header = ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(
                            name,
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color="white",
                        ),
                        ft.Text(
                            f"ID: {p_id}",
                            size=13,
                            color="#b8b8b8",
                        ),
                    ],
                    spacing=2,
                    expand=True,
                ),
                
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        if shiny_exists:
            shiny_img_url = (
                "https://raw.githubusercontent.com/PokeAPI/sprites/master/"
                f"sprites/pokemon/other/home/shiny/{p_id}.png"
            )

            image_section = ft.Row(
    controls=[
        ft.Container(
            width=220,
            padding=12,
            bgcolor="#141414cc",
            border_radius=20,
            content=ft.Column(
                controls=[
                    ft.Image(
                        src=normal_img_url,
                        width=165,
                        height=165,
                        fit=ft.BoxFit.CONTAIN,
                    ),
                    build_image_label("Normal", "#bcbcbc"),
                ],
                spacing=6,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ),
        ft.Container(
            width=220,
            padding=12,
            bgcolor="#1c1810cc",
            border_radius=20,
            content=ft.Column(
                controls=[
                    ft.Image(
                        src=shiny_img_url,
                        width=165,
                        height=165,
                        fit=ft.BoxFit.CONTAIN,
                    ),
                    build_image_label("Shiny ✨", "#ffd966"),
                ],
                spacing=6,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ),
    ],
    spacing=14,
    alignment=ft.MainAxisAlignment.CENTER,
)

            badges = []
            if shiny_status.get("found_wild"):
                badges.append(make_method_badge("🌿", "Vild"))
            if shiny_status.get("found_raid"):
                badges.append(make_method_badge("⚔️", "Raids"))
            if shiny_status.get("found_egg"):
                badges.append(make_method_badge("🥚", "Ägg"))
            if shiny_status.get("found_evolution"):
                badges.append(make_method_badge("🧬", "Utveckling"))
            if shiny_status.get("found_photobomb"):
                badges.append(make_method_badge("📸", "Photobomb"))
            if shiny_status.get("found_research"):
                badges.append(make_method_badge("🔍", "Research"))
            if not badges:
                badges.append(make_method_badge("⭐", "Special/Event"))

            methods_section = ft.Column(
                controls=[
                    ft.Text(
                        "Hittas via",
                        size=13,
                        color="#bdbdbd",
                    ),
                    ft.Row(
                        controls=badges,
                        wrap=True,
                        spacing=10,
                        run_spacing=10,
                    ),
                ],
                spacing=10,
            )

            card_body = ft.Column(
                controls=[
                    header,
                    build_divider(),
                    image_section,
                    build_divider(),
                    methods_section,
                ],
                spacing=16,
            )
        else:
            image_section = ft.Row(
    controls=[
        ft.Container(
            width=260,
            padding=12,
            bgcolor="#141414cc",
            border_radius=20,
            content=ft.Column(
                controls=[
                    ft.Image(
                        src=normal_img_url,
                        width=220,
                        height=180,
                        fit=ft.BoxFit.CONTAIN,
                    ),
                    build_image_label("Normal", "#bcbcbc"),
                ],
                spacing=6,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )
    ],
    alignment=ft.MainAxisAlignment.CENTER,
)

            card_body = ft.Column(
                controls=[
                    header,
                    build_divider(),
                    image_section,
                    build_divider(),
                    ft.Row(
                        controls=[make_no_shiny_badge()],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                spacing=16,
            )

        return ft.Container(
            content=card_body,
            padding=24,
            border_radius=28,
            bgcolor="#000000",
            border=ft.border.all(1, "#202020"),
        )

    def load_data():
        try:
            released_response = requests.get(RELEASED_URL, timeout=10)
            shiny_response = requests.get(SHINY_URL, timeout=10)

            released_response.raise_for_status()
            shiny_response.raise_for_status()

            all_pokemon_db.clear()
            shiny_lookup_db.clear()

            all_pokemon_db.update(released_response.json())
            shiny_lookup_db.update(shiny_response.json())

        except Exception as e:
            results_container.visible = True
            results_list.controls.clear()
            results_list.controls.append(
                ft.Container(
                    content=ft.Text(
                        f"Kunde inte ladda Pokedex: {e}",
                        color="#ff9a9a",
                        size=16,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    padding=20,
                    alignment=ft.Alignment.CENTER,
                )
            )
            page.update()

    def perform_search(e=None):
        results_list.controls.clear()

        query = (search_field.value or "").strip().lower()

        if not query:
            results_container.visible = False
            page.update()
            return

        found_counter = 0

        for p_id, p_info in all_pokemon_db.items():
            name = p_info.get("name", "Okänd")
            p_id_str = str(p_id)

            name_match = query in name.lower()
            id_match = query in p_id_str

            if name_match or id_match:
                found_counter += 1
                shiny_status = shiny_lookup_db.get(p_id)
                results_list.controls.append(
                    build_pokemon_card(p_id, p_info, shiny_status)
                )

        if found_counter == 0:
            results_list.controls.append(
                ft.Container(
                    content=ft.Text(
                        "Inga träffar hittades i Pokedexen.",
                        color="#ff9a9a",
                        size=16,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    padding=20,
                    alignment=ft.Alignment.CENTER,
                )
            )

        results_container.visible = True
        page.update()

    search_field = ft.TextField(
        hint_text="Sök Pokémon eller ID...",
        width=340,
        height=56,
        border=ft.InputBorder.OUTLINE,
        border_radius=28,
        bgcolor="#000000",
        color="white",
        text_size=16,
        content_padding=ft.padding.symmetric(horizontal=20, vertical=16),
        border_color="#333333",
        focused_border_color="#333333",
        focused_border_width=1,
        cursor_color="#ff3b3b",
        on_submit=perform_search,
    )

    search_button = ft.ElevatedButton(
        "SÖK",
        width=180,
        height=46,
        on_click=perform_search,
        style=ft.ButtonStyle(
            bgcolor="#ff3b3b",
            color="white",
            shape=ft.RoundedRectangleBorder(radius=24),
        ),
    )

    hero_content = ft.Container(
        height=520,
        alignment=ft.Alignment.CENTER,
        content=ft.Column(
            controls=[
                ft.Image(
                    src="shinydex.png",
                    width=640,
                    height=220,
                    fit=ft.BoxFit.CONTAIN,
                ),
                ft.Container(height=8),
                ft.Container(
                    content=search_field,
                    
                ),
                ft.Container(height=6),
                ft.Row(
                    controls=[search_button],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            spacing=6,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    scroll_content = ft.Column(
        controls=[
            hero_content,
            results_container,
            ft.Container(height=24),
        ],
        spacing=0,
        scroll=ft.ScrollMode.ADAPTIVE,
        expand=True,
    )

    page.add(
        ft.Stack(
            controls=[
                ft.Container(
                    expand=True,
                    image=ft.DecorationImage(
                        src="bg_groudon.png",
                        fit=ft.BoxFit.COVER,
                        opacity=0.48,
                    ),
                ),
                ft.Container(
                    expand=True,
                    bgcolor="#000000eb",
                ),
                ft.SafeArea(
                    content=scroll_content,
                    expand=True,
                ),
            ],
            expand=True,
        )
    )

    load_data()
    page.update()

#WEB
app = ft.run(main, export_asgi_app=True)

#LOKAL
#ft.app(target=main, assets_dir="assets")
