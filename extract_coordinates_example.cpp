// Exemplo de uso para extrair coordenadas de terreno e objetos
// X-Legend Library - Extração de Coordenadas

#include "FSM.h"
#include <iostream>

int main() {
    Seraph::FSM mapa;
    
    // Carregar arquivo FSM
    std::string arquivoFSM = "meu_mapa.fsm"; // Substitua pelo caminho do seu arquivo
    
    std::cout << "Carregando arquivo FSM: " << arquivoFSM << std::endl;
    
    if (mapa.Load(arquivoFSM)) {
        std::cout << "✅ Arquivo carregado com sucesso!" << std::endl;
        
        // Informações do mapa
        std::cout << "📊 Informações do mapa:" << std::endl;
        std::cout << "   - Heightmaps: " << mapa.GetHeightMapCount() << std::endl;
        std::cout << "   - Objetos: " << mapa.GetObjectCount() << std::endl;
        
        // Extrair coordenadas do terreno
        std::cout << "\n🗺️ Extraindo coordenadas do terreno..." << std::endl;
        if (mapa.ExportTerrainCoordinates("terrain_coordinates.txt")) {
            std::cout << "✅ Coordenadas do terreno salvas em: terrain_coordinates.txt" << std::endl;
        } else {
            std::cout << "❌ Erro ao salvar coordenadas do terreno" << std::endl;
        }
        
        // Extrair coordenadas dos objetos
        std::cout << "\n🏠 Extraindo coordenadas dos objetos..." << std::endl;
        if (mapa.ExportObjectCoordinates("object_coordinates.txt")) {
            std::cout << "✅ Coordenadas dos objetos salvas em: object_coordinates.txt" << std::endl;
        } else {
            std::cout << "❌ Erro ao salvar coordenadas dos objetos" << std::endl;
        }
        
        // Liberar recursos
        mapa.Shutdown();
        
        std::cout << "\n🎉 Extração concluída!" << std::endl;
        std::cout << "\n📁 Arquivos gerados:" << std::endl;
        std::cout << "   - terrain_coordinates.txt (coordenadas X,Y,Z do terreno)" << std::endl;
        std::cout << "   - object_coordinates.txt (coordenadas X,Y,Z dos objetos)" << std::endl;
        
    } else {
        std::cout << "❌ Erro ao carregar arquivo FSM: " << arquivoFSM << std::endl;
        std::cout << "Verifique se o arquivo existe e está no formato correto." << std::endl;
        return -1;
    }
    
    return 0;
}

/*
FORMATO DOS ARQUIVOS GERADOS:

=== terrain_coordinates.txt ===
# Terrain Coordinates Export
# Format: X,Y,Z (Height)
# LayerID,X,Y,Height

# Layer 0 - Width: 256, Height: 256, Scale: 1.0
0,0,0,15.5
0,1,0,15.8
0,2,0,16.1
...

=== object_coordinates.txt ===
# Object Coordinates Export
# Format: ObjectName,X,Y,Z,Rotation,Scale

Tree01,100.5,50.2,200.0,0.0,1.0
Rock02,150.3,45.8,195.5,1.57,0.8
House01,200.0,60.0,180.0,3.14,1.5
...

COMO USAR:
1. Compile este código junto com a biblioteca X-Legend_Lib
2. Substitua "meu_mapa.fsm" pelo caminho do seu arquivo FSM
3. Execute o programa
4. Os arquivos TXT serão gerados na mesma pasta

PRÓXIMOS PASSOS:
- Usar esses arquivos TXT para importar no Blender
- Criar plugin Python que leia essas coordenadas
- Aplicar otimização de cache para objetos duplicados
*/
