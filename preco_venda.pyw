import PySimpleGUI as sg
import pickle

modelos = {}

try:
    with open("modelos.pkl", "rb") as f:
        modelos = pickle.load(f)
except FileNotFoundError:
    pass

def salvar_modelos():
    with open("modelos.pkl", "wb") as f:
        pickle.dump(modelos, f)

def criar_modelo():
    layout_criar_modelo = [
        [sg.Text("Nome do modelo:"), sg.InputText(key="nome_modelo")],
        [sg.Text("Margem de Lucro (ex: 10 para 10%):"), sg.InputText(key="margem_l")],
        [sg.Text("Imposto % (ex: 10 para 10%):"), sg.InputText(key="imposto")],
        [sg.Text("Marketplace % (ex: 10 para 10%):"), sg.InputText(key="taxa_mkt")],
        [sg.Text("Custo Fixo de Embalagem:"), sg.InputText(key="custo_fixo_embalagem")],
        [sg.Text("Taxas de Serviço:"), sg.InputText(key="taxas_de_servico")],
        [sg.Button("Criar Modelo"), sg.Button("Cancelar")]
    ]

    window_criar_modelo = sg.Window("Criar Modelo", layout_criar_modelo)

    while True:
        event, values = window_criar_modelo.read()

        if event == sg.WINDOW_CLOSED or event == "Cancelar":
            break
        elif event == "Criar Modelo":
            nome_modelo = values["nome_modelo"]
            modelos[nome_modelo] = {
                "margem_l": float(values["margem_l"]) / 100,
                "imposto": float(values["imposto"]) / 100,
                "taxa_mkt": float(values["taxa_mkt"]) / 100,
                "custo_fixo_embalagem": float(values["custo_fixo_embalagem"]),
                "taxas_de_servico": float(values["taxas_de_servico"]),
            }
            salvar_modelos()
            sg.popup("Modelo criado com sucesso!")
            break

    window_criar_modelo.close()

def excluir_modelo():
    layout_excluir_modelo = [
        [sg.Text("Selecione um modelo para excluir:")],
        [sg.Listbox(list(modelos.keys()), size=(20, 6), key="modelo_selecionado")],
        [sg.Button("Excluir"), sg.Button("Cancelar")]
    ]

    window_excluir_modelo = sg.Window("Excluir Modelo", layout_excluir_modelo)

    while True:
        event, values = window_excluir_modelo.read()

        if event == sg.WINDOW_CLOSED or event == "Cancelar":
            break
        elif event == "Excluir":
            modelo_selecionado = values["modelo_selecionado"][0]
            if sg.popup_yes_no(f"Tem certeza que deseja excluir o modelo '{modelo_selecionado}'?") == "Yes":
                modelos.pop(modelo_selecionado)
                salvar_modelos()
                sg.popup("Modelo excluído com sucesso!")
            break

    window_excluir_modelo.close()

# Layout da janela principal
layout_principal = [
    [sg.Button("Modelos Salvos"), sg.Button("Criar Modelo"), sg.Button("Excluir Modelo")],
    [sg.Text("", size=(40, 5), key="resultado")],
]

window_principal = sg.Window("Calculadora de Preço de Venda", layout_principal)

while True:
    event, values = window_principal.read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == "Modelos Salvos":
        if not modelos:
            sg.popup("Não há modelos salvos.")
        else:
            layout_selecionar_modelo = [
                [sg.Text("Selecione um ou mais modelos disponíveis:")],
                [sg.Listbox(list(modelos.keys()), size=(20, 6), key="modelos_selecionados", select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE)],
                [sg.Button("Selecionar")]
            ]

            window_selecionar_modelo = sg.Window("Selecionar Modelo", layout_selecionar_modelo)

            while True:
                event, values = window_selecionar_modelo.read()

                if event == sg.WINDOW_CLOSED:
                    break
                elif event == "Selecionar":
                    modelos_selecionados = values["modelos_selecionados"]
                    window_selecionar_modelo.close()
                    break

            if modelos_selecionados:
                preco_custo = float(sg.popup_get_text("Digite o preço de custo:"))
                resultado_calculo = ""

                for modelo_selecionado in modelos_selecionados:
                    modelo = modelos[modelo_selecionado]

                    lucro_minimo = modelo["margem_l"] * preco_custo
                    preco_de_venda = (lucro_minimo + preco_custo + modelo["custo_fixo_embalagem"] + modelo["taxas_de_servico"]) / (1 - (modelo["imposto"] + modelo["taxa_mkt"]))
                    taxas = preco_de_venda * (modelo["imposto"] + modelo["taxa_mkt"])
                    lucro = preco_de_venda - taxas - preco_custo - modelo["custo_fixo_embalagem"] - modelo["taxas_de_servico"]

                    resultado_calculo += f"Modelo: {modelo_selecionado}\n"
                    resultado_calculo += f"Preço de venda: R${preco_de_venda:.2f}\n"
                    resultado_calculo += f"Taxas: R${taxas:.2f}\n"
                    resultado_calculo += f"Lucro: R${lucro:.2f}\n"
                    resultado_calculo += f"Custo Fixo de Embalagem: R${modelo['custo_fixo_embalagem']:.2f}\n"
                    resultado_calculo += f"Taxas de Serviço: R${modelo['taxas_de_servico']:.2f}\n\n"

                sg.popup_scrolled(resultado_calculo, title="Resultado do Cálculo")

            window_selecionar_modelo.close()
    elif event == "Criar Modelo":
        criar_modelo()
    elif event == "Excluir Modelo":
        if not modelos:
            sg.popup("Não há modelos para excluir.")
        else:
            excluir_modelo()

window_principal.close()
