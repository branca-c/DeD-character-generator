from character_service import (
    create_character,
    save_character,
    list_characters,
    get_character,
    delete_character,
    regenerate_backstory_for_id,
)
import ui


def main():
    ui.header("D&D Character Generator CLI")

    while True:
        ui.menu()
        choice = ui.ask("👉 Inserisci scelta (0-5):")

        if choice == "0":
            print("\n👋 Ciao! Alla prossima.")
            return

        if choice == "1":
            prompt = ui.ask("🧠 Descrivi il personaggio (es: 'un mago misterioso con un passato oscuro'):")
            if not prompt:
                print("⚠️ Inserisci una descrizione valida.")
                continue
            try:
                c = create_character(prompt)
                ui.show_character(c)

                save = ui.ask("\n💾 Vuoi salvare questo personaggio? (s/n):").lower()
                if save == "s":
                    save_character(c)
                    print("✅ Salvato su db.json")
                else:
                    print("ℹ️ Non salvato.")
            except Exception as e:
                print(f"❌ Errore: {e}")

        elif choice == "2":
            chars = list_characters()
            ui.show_list(chars)

        elif choice == "3":
            cid = ui.ask("🆔 Inserisci ID personaggio:")
            c = get_character(cid)
            if not c:
                print("❌ Personaggio non trovato.")
            else:
                ui.show_character(c)

        elif choice == "4":
            cid = ui.ask("🆔 Inserisci ID da cancellare:")
            ok = delete_character(cid)
            if ok:
                print("🗑️ Personaggio cancellato.")
            else:
                print("❌ Personaggio non trovato.")

        elif choice == "5":
            cid = ui.ask("🆔 Inserisci ID per rigenerare la backstory:")
            try:
                c = regenerate_backstory_for_id(cid)
                print("✅ Backstory aggiornata!")
                ui.show_character(c)
            except Exception as e:
                print(f"❌ Errore: {e}")

        else:
            print("⚠️ Scelta non valida. Riprova.")


if __name__ == "__main__":
    main()
