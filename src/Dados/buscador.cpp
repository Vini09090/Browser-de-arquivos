#include <algorithm>
#include <cctype>
#include <filesystem>
#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
#include "Files.h"

namespace fs = std::filesystem;
const char* home = std::getenv("HOME");
const std::string RAIZ = home ? home : "";


const std::string RAIZ = home;

std::string normalizar_nome(std::string texto) {
    std::string resultado;

    for (unsigned char c : texto) {
        if (std::isalnum(c))
            resultado += static_cast<char>(std::tolower(c));
    }

    return resultado;
}

std::vector<std::string> getBigrams(const std::string& texto) {
    std::vector<std::string> pares;
    if (texto.size() < 2)
        return pares;

    for (std::size_t i = 0; i + 1 < texto.size(); ++i)
        pares.push_back(texto.substr(i, 2));

    return pares;
}

double calculateSimilarity(const std::string& str1, const std::string& str2) {
    std::string a = normalizar_nome(str1);
    std::string b = normalizar_nome(str2);

    if (a.empty() || b.empty())
        return 0.0;

    if (a == b)
        return 1.0;

    if (a.size() < 2 || b.size() < 2)
        return b.find(a) != std::string::npos ? 1.0 : 0.0;

    auto bigramsA = getBigrams(a);
    auto bigramsB = getBigrams(b);

    int intersecao = 0;

    for (const auto& par : bigramsA) {
        if (std::find(bigramsB.begin(), bigramsB.end(), par) != bigramsB.end())
            ++intersecao;
    }

    int uniao = static_cast<int>(
        bigramsA.size() + bigramsB.size() - intersecao
    );

    if (uniao == 0)
        return 0.0;

    double similaridade = (2.0 * intersecao) / uniao;

    if (b.find(a) != std::string::npos)
        similaridade = std::max(similaridade, 0.80);

    return similaridade;
}

struct Resultado {
    std::string caminho;
    std::string titulo;
    double similaridade;
};

int main(int argc, char* argv[]) {
    if (argc < 2 || std::string(argv[1]).empty())
        return 0;

    std::string termo = argv[1];

    std::vector<std::string> extensoes{
        ".pdf", ".epub", ".txt", ".doc", ".docx"
    };

    auto arquivos = buscar_arquivos(RAIZ, extensoes);
    std::vector<Resultado> resultados;

    for (const auto& arquivo : arquivos) {
        fs::path caminho(arquivo);
        std::string titulo = caminho.stem().string();

        double similaridade = calculateSimilarity(termo, titulo);

        // 0.20 = 20%
        if (similaridade >= 0.20) {
            resultados.push_back({arquivo, titulo, similaridade});
        }
    }

    std::sort(resultados.begin(), resultados.end(),
        [](const Resultado& a, const Resultado& b) {
            return a.similaridade > b.similaridade;
        });

    for (const auto& resultado : resultados) {
        std::cout << resultado.similaridade << "|"
                  << resultado.titulo << "|"
                  << resultado.caminho << '\n';
    }

    return 0;
}
