import flet as ft
import requests

def main(page: ft.Page):
    # --- 1. Proffsiga Grundinställningar ---
    page.title = "Shinydex"
    page.favicon = "assets/icon.png"
    page.web_manifest = "assets/manifest.json"
    page.theme_mode = "dark"
    page.bgcolor = "#000000"
    page.padding = 0
    page.scroll = "adaptive"

    results_list = ft.Column(spacing=15)

    # --- 2. Ladda data ---
    all_pokemon_db = {}
    shiny_lookup_db = {}

    url_all = "https://pogoapi.net/api/v1/released_pokemon.json"
    url_shiny = "https://pogoapi.net/api/v1/shiny_pokemon.json"

    try:
        all_pokemon_db.update(requests.get(url_all).json())
        shiny_lookup_db.update(requests.get(url_shiny).json())
    except Exception as e:
        results_list.controls.append(
            ft.Text(f"Kunde inte ladda Pokedex: {e}", color="red", size=16)
        )

    # --- BADGES ---
    def make_method_badge(emoji, text_value):
        return ft.Container(
            content=ft.Text(f"{emoji} {text_value}", color="white", size=13, weight="bold"),
            padding=10,
            bgcolor="#383838",
            border_radius=20
        )

    def make_no_shiny_badge():
        return ft.Container(
            content=ft.Text("❌ Finns ej som shiny", color="#ff8888", size=13, weight="bold"),
            padding=10,
            bgcolor="#3a1111",
            border_radius=20
        )

    # --- SÖK ---
    def perform_search(e=None):
        results_list.controls.clear()
        query = search_field.value.lower().strip()

        if not query:
            page.update()
            return

        found_counter = 0

        for p_id, p_info in all_pokemon_db.items():
            name = p_info.get("name", "Okänd")

            if query in name.lower():
                found_counter += 1

                shiny_status = shiny_lookup_db.get(p_id)
                shiny_exists = shiny_status is not None

                normal_img_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/{p_id}.png"

                card = ft.Container(
                    content=ft.Text(name),
                    padding=10,
                    bgcolor="#222",
                    border_radius=10
                )

                results_list.controls.append(card)

        if found_counter == 0:
            results_list.controls.append(
                ft.Text("Inga träffar hittades", color="red")
            )

        page.update()

    # --- INPUT ---
    search_field = ft.TextField(
        label="Sök Pokémon...",
        width=300,
        border_radius=20,
        on_submit=perform_search
    )

    search_button = ft.ElevatedButton(
        "SÖK",
        width=300,
        height=50,
        on_click=perform_search
    )

    # --- HERO (FIXAD VERSION) ---
    hero = ft.Container(
        expand=True,
        content=ft.Column(
            [
                # Bakgrund (pokeball)
                ft.Container(
                    expand=True,
                    alignment=ft.alignment.center,
                    content=ft.Image(
                        src="assets/icon.png",
                        width=600,   # större
                        opacity=0.08  # mycket svagare
                    )
                ),

                # UI ovanpå (centrerat)
                ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.Column(
                        [
                            ft.Text("Shinydex", size=30, weight="bold"),
                            search_field,
                            search_button,
                        ],
                        horizontal_alignment="center",
                        spacing=20
                    )
                )
            ],
            alignment="center",
            horizontal_alignment="center"
        )
    )

    page.add(hero, results_list)

app = ft.run(main, export_asgi_app=True)
