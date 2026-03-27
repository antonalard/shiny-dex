import flet as ft
import requests

def main(page: ft.Page):
    # --- 1. Grundinställningar ---
    page.title = "Shinydex"
    page.favicon = "assets/icon.png"
    page.web_manifest = "assets/manifest.json"
    page.theme_mode = "dark"
    page.bgcolor = "#000000"
    page.padding = 0
    page.scroll = "adaptive"

    results_list = ft.Column(spacing=20)

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
            content=ft.Text(
                f"{emoji} {text_value}",
                color="white",
                size=12,
                weight="bold",
            ),
            padding=ft.padding.only(left=12, right=12, top=8, bottom=8),
            bgcolor="#1f1f1f",
            border_radius=20,
            border=ft.border.all(1, "#2d2d2d"),
        )

    def make_no_shiny_badge():
        return ft.Container(
            content=ft.Text(
                "❌ Finns ej som shiny",
                color="#ff9c9c",
                size=12,
                weight="bold",
            ),
            padding=ft.padding.only(left=12, right=12, top=8, bottom=8),
            bgcolor="#2a1010",
            border_radius=20,
            border=ft.border.all(1, "#4a1d1d"),
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

                normal_img_url = (
                    f"https://raw.githubusercontent.com/PokeAPI/sprites/master/"
                    f"sprites/pokemon/other/home/{p_id}.png"
                )

                card_content_children = [
                    ft.Row(
                        [
                            ft.Text(name, size=24, weight="bold", color="white"),
                            ft.Text(f"ID: {p_id}", color="#8f8f8f", size=14),
                        ],
                        alignment="spaceBetween",
                    ),
                    ft.Divider(color="#2a2a2a"),
                ]

                if shiny_exists:
                    shiny_img_url = (
                        f"https://raw.githubusercontent.com/PokeAPI/sprites/master/"
                        f"sprites/pokemon/other/home/shiny/{p_id}.png"
                    )

                    card_content_children.append(
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Image(
                                            src=normal_img_url,
                                            width=155,
                                            height=155,
                                            fit="contain",
                                        ),
                                        ft.Text("Normal", size=12, color="#9a9a9a"),
                                    ],
                                    alignment="center",
                                    horizontal_alignment="center",
                                ),
                                ft.Column(
                                    [
                                        ft.Image(
                                            src=shiny_img_url,
                                            width=155,
                                            height=155,
                                            fit="contain",
                                        ),
                                        ft.Text("Shiny ✨", size=12, color="#ffd966"),
                                    ],
                                    alignment="center",
                                    horizontal_alignment="center",
                                ),
                            ],
                            alignment="center",
                            spacing=16,
                        )
                    )

                    card_content_children.append(ft.Divider(color="#2a2a2a"))
                    card_content_children.append(
                        ft.Text("Hittas via:", size=14, color="#9a9a9a")
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

                    method_rows = ft.Column(spacing=10)
                    current_row = ft.Row(spacing=10)

                    for i, badge in enumerate(badges):
                        current_row.controls.append(badge)
                        if len(current_row.controls) == 3 or i == len(badges) - 1:
                            method_rows.controls.append(current_row)
                            current_row = ft.Row(spacing=10)

                    card_content_children.append(method_rows)

                else:
                    card_content_children.append(
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Image(
                                            src=normal_img_url,
                                            width=210,
                                            height=170,
                                            fit="contain",
                                        ),
                                        ft.Text("Normal", size=12, color="#9a9a9a"),
                                    ],
                                    alignment="center",
                                    horizontal_alignment="center",
                                )
                            ],
                            alignment="center",
                        )
                    )

                    card_content_children.append(ft.Divider(color="#2a2a2a"))
                    card_content_children.append(
                        ft.Row([make_no_shiny_badge()], alignment="center")
                    )

                result_card = ft.Container(
                    content=ft.Column(
                        controls=card_content_children,
                        spacing=6,
                    ),
                    padding=22,
                    border_radius=24,
                    bgcolor="#101010dd",
                    border=ft.border.all(1, "#2a2a2a"),
                )

                results_list.controls.append(result_card)

        if found_counter == 0:
            results_list.controls.append(
                ft.Text(
                    "Inga träffar hittades i Pokedexen.",
                    color="#ff7d7d",
                    size=16,
                )
            )

        page.update()

    # --- INPUT ---
    search_field = ft.TextField(
        hint_text="Sök Pokémon...",
        width=340,
        border_radius=28,
        bgcolor="#0b0b0bcc",
        color="white",
        text_size=16,
        content_padding=16,
        border_color="#2f2f2f",
        focused_border_color="#ff3b3b",
        on_submit=perform_search,
    )

    search_button = ft.ElevatedButton(
        "SÖK",
        width=340,
        height=54,
        on_click=perform_search,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=28),
            bgcolor="#ff3b3b",
            color="white",
            text_style=ft.TextStyle(size=16, weight="bold"),
        ),
    )

    # --- HERO MED RIKTIG BAKGRUND ---
    hero = ft.Container(
        height=560,
        content=ft.Stack(
            controls=[
                # Bakgrundsbild
                ft.Image(
                    src="assets/bg_groudon.png",
                    width=1200,
                    height=560,
                    fit="cover",
                ),

                # Mörk overlay ovanpå bilden
                ft.Container(
                    width=1200,
                    height=560,
                    bgcolor="#000000aa",
                ),

                # Innehåll i mitten
                ft.Container(
                    width=1200,
                    height=560,
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "Shinydex",
                                size=36,
                                weight="bold",
                                color="white",
                                text_align="center",
                            ),
                            search_field,
                            search_button,
                        ],
                        alignment="center",
                        horizontal_alignment="center",
                        spacing=22,
                    ),
                ),
            ]
        )
    )

    results_section = ft.Container(
        padding=20,
        content=results_list,
    )

    page.add(
        hero,
        results_section,
    )

app = ft.run(main, export_asgi_app=True)
