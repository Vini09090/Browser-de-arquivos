#ifndef FILES_H
#define FILES_H

#include <string>
#include <vector>
#include <filesystem>
#include <algorithm>
#include <cctype>

namespace fs = std::filesystem;



inline std::string para_minusculas(const std::string& texto)
{
    std::string resultado = texto;

    std::transform(
        resultado.begin(),
        resultado.end(),
        resultado.begin(),
        [](unsigned char c)
        {
            return static_cast<char>(std::tolower(c));
        }
    );

    return resultado;
}


inline std::vector<std::string> buscar_arquivos(
    const std::string& caminho,
    const std::vector<std::string>& extensoes
)
{
    std::vector<std::string> resultado;

    if (!fs::exists(caminho) || !fs::is_directory(caminho))
    {
        return resultado;
    }

    for (
        const auto& entry :
        fs::recursive_directory_iterator(
            caminho,
            fs::directory_options::skip_permission_denied
        )
    )
    {
        if (!entry.is_regular_file())
        {
            continue;
        }

        std::string extensao =
            para_minusculas(
                entry.path().extension().string()
            );

        for (const std::string& permitida : extensoes)
        {
            if (
                extensao ==
                para_minusculas(permitida)
            )
            {
                resultado.push_back(
                    entry.path().string()
                );

                break;
            }
        }
    }

    return resultado;
}

