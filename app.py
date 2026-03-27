import flet as ft
import requests

def main(page: ft.Page):
    page.title = "Shinydex"
    page.favicon = "assets/icon.png"
    page.web_manifest = "assets/manifest.json"
    page.theme_mode = "dark"
    page.bgcolor = "#000000"
    page.padding = 0
    page.scroll = "adaptive"

    results_list = ft.Column(spacing=20)

    # --- DATA ---
    all_pokemon_db = {}
    shiny_lookup_db = {}

    url_all = "https://pogoapi.net/api/v1/released_pokemon.json"
    url_shiny = "https://pogoapi.net/api/v1/shiny_pokemon.json"

    try:
        all_pokemon_db.update(requests.get(url_all).json())
        shiny_lookup_db.update(requests.get(url_shiny).json())
    except Exception as e:
        results_list.controls.append(
            ft.Text(f"Kunde inte ladda Pokedex: {e}", color="red")
        )

    # --- BADGES ---
    def make_method_badge(emoji, text_value):
        return ft.Container(
            content=ft.Text(f"{emoji} {text_value}", size=12, weight="bold"),
            padding=8,
            bgcolor="#2a2a2a",
            border_radius=20,
        )

    def make_no_shiny_badge():
        return ft.Container(
            content=ft.Text("❌ Ej shiny", size=12, weight="bold"),
            padding=8,
            bgcolor="#3a1111",
            border_radius=20,
        )

    # --- SÖK ---
    def perform_search(e=None):
        results_list.controls.clear()
        query = search_field.value.lower().strip()

        if not query:
            page.update()
            return

        for p_id, p_info in all_pokemon_db.items():
            name = p_info.get("name", "Okänd")

            if query in name.lower():
                shiny_status = shiny_lookup_db.get(p_id)
                shiny_exists = shiny_status is not None

                normal_img = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/{p_id}.png"

                card = ft.Container(
                    padding=20,
                    border_radius=20,
                    bgcolor="#111111",
                    border=ft.border.all(1, "#2a2a2a"),
                    content=ft.Column(
                        [
                            # Namn
                            ft.Text(name, size=24, weight="bold"),

                            # Bild(er)
                            ft.Row(
                                [
                                    ft.Image(src=normal_img, width=150),
                                    ft.Image(
                                        src=f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/shiny/{p_id}.png",
                                        width=150,
                                    ) if shiny_exists else ft.Container()
                                ],
                                alignment="center"
                            ),

                            # Badge
                            ft.Row(
                                [make_no_shiny_badge()] if not shiny_exists else [],
                                alignment="center"
                            )
                        ],
                        spacing=10
                    )
                )

                results_list.controls.append(card)

        page.update()

    # --- INPUT ---
    search_field = ft.TextField(
        hint_text="Sök Pokémon...",
        width=300,
        border_radius=25,
        bgcolor="#111111",
        color="white",
        text_size=16,
        content_padding=15,
        on_submit=perform_search,
    )

    search_button = ft.Container(
        content=ft.Text("SÖK", weight="bold"),
        width=300,
        height=50,
        alignment=ft.alignment.center,
        bgcolor="#ff3b3b",
        border_radius=25,
        on_click=perform_search,
    )

    # --- HERO (GLASS STYLE) ---
    hero = ft.Container(
        height=500,
        content=ft.Stack(
            [
                # Bakgrund
                ft.Container(
                    content=ft.Image(
                        src="assets/icon.png",
                        width=700,
                        opacity=0.06,
                    ),
                    alignment=ft.alignment.center
                ),

                # UI ovanpå
                ft.Column(
                    [
                        ft.Text("Shinydex", size=32, weight="bold"),
                        search_field,
                        search_button,
                    ],
                    alignment="center",
                    horizontal_alignment="center",
                    spacing=20
                )
            ]
        )
    )

    page.add(
        hero,
        ft.Container(padding=20, content=results_list)
    )

ft.app(target=main)
