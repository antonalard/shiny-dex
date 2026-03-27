import flet as ft


def main(page: ft.Page):
    page.title = "Shinydex Mockup"
    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#000000"
    page.theme_mode = ft.ThemeMode.DARK

    search_field = ft.TextField(
        hint_text="Sök Pokémon...",
        width=340,
        height=56,
        border=ft.InputBorder.OUTLINE,
        border_radius=28,
        bgcolor="#111111cc",
        color="white",
        text_size=16,
        content_padding=ft.padding.symmetric(horizontal=20, vertical=16),
        border_color="#333333",
        focused_border_color="#333333",
        focused_border_width=1,
        cursor_color="#ff3b3b",
    )

    search_button = ft.ElevatedButton(
        "SÖK",
        width=180,
        height=46,
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
                    padding=8,
                    bgcolor="#00000055",
                    border_radius=36,
                    border=ft.border.all(1, "#ffffff18"),
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

    def mock_badge(text_value):
        return ft.Container(
            content=ft.Text(
                text_value,
                color="white",
                size=11,
                weight=ft.FontWeight.BOLD,
            ),
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
            bgcolor="#171717cc",
            border_radius=18,
            border=ft.border.all(1, "#2a2a2a"),
        )

    def mock_card(name, pokemon_id, shiny=True):
        badge_text = "✨ Shiny" if shiny else "—"
        badge_text_color = "#ffd966" if shiny else "#aaaaaa"
        badge_bg = "#2a2412cc" if shiny else "#151515cc"
        badge_border = "#5a4a1a" if shiny else "#2a2a2a"

        right_panel_bg = "#1c1810cc" if shiny else "#141414cc"
        right_label = "Shiny ✨" if shiny else "Variant"
        right_label_color = "#ffd966" if shiny else "#bcbcbc"

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
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
                                        f"ID: {pokemon_id}",
                                        size=13,
                                        color="#b8b8b8",
                                    ),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            ft.Container(
                                content=ft.Text(
                                    badge_text,
                                    size=11,
                                    color=badge_text_color,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                padding=ft.padding.symmetric(
                                    horizontal=12,
                                    vertical=8,
                                ),
                                bgcolor=badge_bg,
                                border_radius=18,
                                border=ft.border.all(1, badge_border),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(
                        height=1,
                        bgcolor="#1f1f1f",
                        border_radius=10,
                    ),
                    ft.Row(
                        controls=[
                            ft.Container(
                                expand=True,
                                padding=12,
                                bgcolor="#141414cc",
                                border_radius=20,
                                content=ft.Column(
                                    controls=[
                                        ft.Container(
                                            height=165,
                                            alignment=ft.Alignment.CENTER,
                                            content=ft.Text(
                                                "Bild",
                                                color="#666666",
                                                size=18,
                                            ),
                                        ),
                                        ft.Text(
                                            "Normal",
                                            size=11,
                                            color="#bcbcbc",
                                            text_align=ft.TextAlign.CENTER,
                                        ),
                                    ],
                                    spacing=6,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                            ),
                            ft.Container(
                                expand=True,
                                padding=12,
                                bgcolor=right_panel_bg,
                                border_radius=20,
                                content=ft.Column(
                                    controls=[
                                        ft.Container(
                                            height=165,
                                            alignment=ft.Alignment.CENTER,
                                            content=ft.Text(
                                                "Bild",
                                                color="#666666",
                                                size=18,
                                            ),
                                        ),
                                        ft.Text(
                                            right_label,
                                            size=11,
                                            color=right_label_color,
                                            text_align=ft.TextAlign.CENTER,
                                        ),
                                    ],
                                    spacing=6,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                            ),
                        ],
                        spacing=14,
                        alignment=ft.MainAxisAlignment.CENTER,
                        wrap=True,
                    ),
                    ft.Container(
                        height=1,
                        bgcolor="#1f1f1f",
                        border_radius=10,
                    ),
                    ft.Text(
                        "Mockup-sektion",
                        size=13,
                        color="#bdbdbd",
                    ),
                    ft.Row(
                        controls=[
                            mock_badge("🌿 Vild"),
                            mock_badge("⚔️ Raids"),
                            mock_badge("🔍 Research"),
                        ],
                        wrap=True,
                        spacing=10,
                        run_spacing=10,
                    ),
                ],
                spacing=16,
            ),
            padding=24,
            border_radius=28,
            bgcolor="#0d0d0dde",
            border=ft.border.all(1, "#202020"),
        )

    results_section = ft.Container(
        padding=ft.padding.symmetric(horizontal=20, vertical=20),
        content=ft.Column(
            controls=[
                mock_card("Pikachu", "25", shiny=True),
                mock_card("Mewtwo", "150", shiny=False),
                mock_card("Charizard", "6", shiny=True),
                mock_card("Gengar", "94", shiny=True),
                mock_card("Lucario", "448", shiny=False),
                mock_card("Rayquaza", "384", shiny=True),
            ],
            spacing=18,
        ),
    )

    scroll_content = ft.Column(
        controls=[
            hero_content,
            results_section,
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


ft.app(target=main, assets_dir="assets")
