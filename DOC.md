# Documentação da X-Legend Library

## Visão Geral

A **X-Legend Library** é uma biblioteca C++ desenvolvida para trabalhar com diferentes tipos de arquivos utilizados em jogos da X-Legend, especificamente testada com arquivos do Grand Fantasia. A biblioteca oferece funcionalidades para leitura, manipulação e escrita de arquivos FSM (mapas), SMP (small maps) e PKG (packages/arquivos compactados).

**Autor:** Azazel  
**Plataforma:** Windows  
**Linguagem:** C++  
**Tipo de Projeto:** Biblioteca Estática (.lib)

## Arquitetura da Biblioteca

A biblioteca está organizada no namespace `Seraph` e consiste em várias classes especializadas:

### Estrutura de Diretórios

```
X-Legend_Lib/
├── include/          # Arquivos de cabeçalho (.h)
├── source/           # Implementações (.cpp)
├── Debug/            # Builds de debug (x86/x64)
├── Release/          # Builds de release (x86/x64)
├── zlib/             # Dependência para compressão
└── X-Legend.vcxproj  # Projeto Visual Studio
```

## Classes Principais

### 1. Classe FSM (File System Map)

**Localização:** `FSM.h` / `FSM.cpp`  
**Propósito:** Manipulação de arquivos de mapa do jogo

#### Estruturas de Dados

```cpp
struct CoreHeader {
    char Signature[0x54];      // Assinatura do arquivo
    long HeightmapCount;       // Número de heightmaps
} m_FSMHeader;

struct HeightMapHeader {
    char Signature[4];         // Assinatura da seção
    unsigned long LinearSz;    // Tamanho linear dos dados
    unsigned long Width;       // Largura do mapa
    unsigned long Height;      // Altura do mapa
    float Scale;              // Escala do terreno
} *m_HeightMapHeader;

struct ObjectHeader {
    char Signature[4];         // Assinatura da seção
    unsigned long LinearSz;    // Tamanho linear dos dados
    unsigned long ObjectCount; // Número de objetos
} m_ObjectHeader;

struct HeightMapType {
    float HeightMap;          // Altura do terreno
    unsigned char RGBA[4];    // Cores RGBA
} **HeightMap;

struct ObjectType {
    float X, Y, Z;           // Posição 3D
    float Rotation;          // Rotação (em radianos)
    float Scale;             // Escala do objeto
    char Name[STRINGSZ];     // Nome do objeto (40 bytes)
} *Object;
```

#### Funcionalidades Principais

1. **Carregamento de Arquivos FSM**
   ```cpp
   bool Load(std::string FilePath);
   ```
   - Lê a estrutura completa do arquivo FSM
   - Carrega heightmaps, texturas e objetos
   - Aloca memória dinamicamente

2. **Salvamento de Arquivos FSM**
   ```cpp
   bool Save(std::string OutputPath);
   ```
   - Escreve estrutura FSM modificada
   - Inclui objetos importados adicionalmente

3. **Exportação de Heightmaps como BMP**
   ```cpp
   bool ExportHeightMapAsBMP(std::string FilePath);
   ```
   - Converte dados de altura para formato bitmap
   - Gera arquivo BMP para cada layer de heightmap

4. **Importação de Heightmaps de BMP**
   ```cpp
   bool ImportHeightMapFromBMP(std::string FilePath, long HeightMapSlotID);
   ```
   - Substitui heightmap existente com dados de imagem BMP
   - **ATENÇÃO:** Funcionalidade em demo, pode ter falhas

5. **Exportação para ASCII**
   ```cpp
   bool AsASCIIFile(bool WriteHeightmap = false);
   ```
   - Gera arquivo texto com informações dos objetos
   - Opcionalmente inclui dados de heightmap

6. **Importação de Objetos**
   ```cpp
   bool ImportObject(float X, float Y, float Z, float Rotation, float Scale, const char* Name);
   ```
   - Adiciona novos objetos ao mapa
   - Objetos são salvos quando o arquivo é exportado

#### Métodos Getter

```cpp
long GetHeightMapCount();                    // Número de heightmaps
long GetWidthAt(int HeightMapID);           // Largura de um heightmap
long GetHeightAt(int HeightMapID);          // Altura de um heightmap
long GetScaleAt(int HeightMapID);           // Escala de um heightmap
long GetMaterialCountAt(int TextureLayerID); // Número de materiais em uma camada
long GetObjectCount();                       // Número total de objetos
```

### 2. Classe SMP (Small Map)

**Localização:** `SMP.h` / `SMP.cpp`  
**Propósito:** Manipulação de arquivos de mapas pequenos/minimapas

#### Estrutura de Dados

```cpp
class SMP {
    short SignatureSz;        // Tamanho da assinatura
    char* Signature;          // Assinatura do arquivo
    short LinkSz;            // Tamanho do link
    char* Link;              // Link/referência
    
    struct Header {
        short Width, Height;  // Dimensões do mapa
        long LinearSz;       // Tamanho linear dos dados
    } m_Header;
    
    char* Data;              // Dados da imagem
};
```

#### Funcionalidades

1. **Carregamento**
   ```cpp
   bool Load(std::string FilePath);
   ```
   - Lê arquivo SMP completo
   - Processa assinatura, link e dados de imagem

2. **Salvamento**
   ```cpp
   bool Save(std::string OutputPath);
   ```
   - Escreve arquivo SMP modificado

3. **Exportação como BMP**
   ```cpp
   bool ExportAsBMP(std::string OutputPath);
   ```
   - Converte dados SMP para formato bitmap

4. **Remoção de Colisão**
   ```cpp
   void RemoveCollision();
   ```
   - Zera dados de colisão do mapa

### 3. Classe PKG (Package)

**Localização:** `PKG.h` / `PKG.cpp`  
**Propósito:** Manipulação de arquivos compactados do jogo

#### Estruturas de Dados

```cpp
struct IdxSignature {
    uint Dummy[0x41];        // Dados dummy
    char Signature[0xC];     // Assinatura
    uint Unknown2-6;         // Campos desconhecidos
} Signature;

struct FileHeader {
    uint FileID;             // ID do arquivo
    uint Offset;             // Offset no arquivo PKG
    uint Unk4;              // Campo desconhecido
    uint SizePacked;        // Tamanho comprimido
    uint Unk6-9;            // Campos desconhecidos
    time_t PackTime;        // Tempo de empacotamento
    time_t OpenTime;        // Tempo de abertura
    time_t ChangeTime;      // Tempo de modificação
    uint SizeOriginal;      // Tamanho original
    char FileName[0x104];   // Nome do arquivo
    char FilePath[0x104];   // Caminho do arquivo
    uint Unk1;              // Campo desconhecido
    uint pkgNum;            // Número do pacote
    uint FileCRC;           // CRC do arquivo
} Header;
```

#### Funcionalidades

1. **Processamento Principal**
   ```cpp
   bool Load(bool Unpack = false);
   ```
   - `Unpack = false`: Comprime arquivos da pasta atual para PKG
   - `Unpack = true`: Descomprime arquivos PKG para pasta atual

2. **Compressão (Métodos Internos)**
   ```cpp
   bool EncodeFile();      // Comprime arquivo individual
   bool Encrypt();         // Processo completo de compressão
   bool WritePacked();     // Escreve dados comprimidos
   ```

3. **Descompressão (Métodos Internos)**
   ```cpp
   bool DecodeFile();      // Descomprime arquivo individual
   bool Decrypt();         // Processo completo de descompressão
   bool WriteUnpacked();   // Escreve arquivo descomprimido
   ```

**⚠️ IMPORTANTE:** A funcionalidade PKG está em versão demo e pode não ser 100% confiável.

### 4. Classes Auxiliares

#### Classe File

**Localização:** `File.h`  
**Propósito:** Wrapper para operações de arquivo com tratamento de erro

- Estende `std::fstream` com verificação automática de erros
- Templates para leitura/escrita tipada
- Métodos `open`, `read`, `write`, `get` com validação

#### Classe BMP

**Localização:** `BMP.h` / `BMP.cpp`  
**Propósito:** Manipulação de arquivos bitmap

```cpp
class BMP {
public:
    BITMAPFILEHEADER Header;  // Cabeçalho do arquivo BMP
    BITMAPINFOHEADER Info;    // Informações da imagem
    char* Data;               // Dados da imagem
    
    bool Import(std::string FilePath);  // Importa BMP existente
    bool Export(std::string FilePath, int Width, int Height, char* Data);  // Exporta BMP
};
```

#### Sistema de Tratamento de Erros

**Localização:** `Error.h`  
**Propósito:** Macros para tratamento de erros

```cpp
// Macros de debug (ativas apenas em _DEBUG)
#define Assert(Expr)                    // Verificação simples
#define AssertC(Expr, Code)            // Verificação com código de erro
#define AssertM(Expr, Message)         // Verificação com mensagem
#define AssertCM(Expr, Code, Message)  // Verificação completa
```

- Em modo debug: Exibe MessageBox com detalhes do erro
- Em modo release: Verificação simplificada

## Fluxo de Trabalho Típico

### Trabalhando com FSM

1. **Carregamento e Análise**
   ```cpp
   Seraph::FSM mapa;
   mapa.Load("meu_mapa.fsm");
   
   // Obter informações
   int numHeightmaps = mapa.GetHeightMapCount();
   int numObjetos = mapa.GetObjectCount();
   ```

2. **Exportação de Dados**
   ```cpp
   // Exportar heightmaps como imagens
   mapa.ExportHeightMapAsBMP("heightmap_");
   
   // Gerar relatório em texto
   mapa.AsASCIIFile(true);  // com heightmap
   ```

3. **Modificação e Salvamento**
   ```cpp
   // Adicionar novos objetos
   mapa.ImportObject(100.0f, 50.0f, 200.0f, 0.0f, 1.0f, "MeuObjeto");
   
   // Salvar modificações
   mapa.Save("mapa_modificado.fsm");
   ```

### Trabalhando com SMP

```cpp
Seraph::SMP miniMapa;
miniMapa.Load("minimapa.smp");
miniMapa.ExportAsBMP("minimapa.bmp");  // Visualizar como imagem
miniMapa.RemoveCollision();            // Remover dados de colisão
miniMapa.Save("minimapa_sem_colisao.smp");
```

### Trabalhando com PKG

```cpp
Seraph::PKG pacote;

// Descomprimir arquivos PKG
pacote.Load(true);   // Extrai todos os arquivos

// Recomprimir arquivos (após modificações)
pacote.Load(false);  // Comprime arquivos da pasta atual
```

## Limitações e Considerações

1. **Compatibilidade**: Testado apenas com Grand Fantasia, pode não funcionar com outros jogos X-Legend (AK, EE)

2. **Estado de Desenvolvimento**:
   - FSM: Funcionalidade completa de leitura, parcial de escrita
   - SMP: Funcionalidade básica de leitura/escrita
   - PKG: Versão demo, pode apresentar instabilidades

3. **Dependências**:
   - Windows API (para MessageBox e operações de arquivo)
   - zlib (para compressão PKG)
   - Visual Studio (projeto configurado para v142 toolset)

4. **Gerenciamento de Memória**:
   - Alocação dinâmica extensiva
   - Importante chamar `Shutdown()` para liberar recursos
   - Alguns vazamentos potenciais em cenários de erro

5. **Formato de Arquivos**:
   - Estruturas binárias específicas do jogo
   - Alguns campos ainda desconhecidos (marcados como "Unk")
   - Engenharia reversa baseada em observação

## Compilação e Uso

### Requisitos

- Visual Studio 2019 ou superior
- Windows SDK 10.0
- zlib library (para funcionalidade PKG)

### Configurações de Build

- **Tipo**: Biblioteca Estática (.lib)
- **Plataformas**: x86, x64
- **Configurações**: Debug, Release
- **Character Set**: Unicode

### Uso em Projetos

1. Incluir cabeçalhos necessários
2. Linkar com a biblioteca compilada
3. Garantir que zlib esteja disponível (para PKG)

## Exemplos Práticos

### Exemplo 1: Análise Completa de Mapa

```cpp
#include "FSM.h"
#include <iostream>

int main() {
    Seraph::FSM mapa;
    
    if (mapa.Load("world01.fsm")) {
        std::cout << "Mapa carregado com sucesso!\n";
        std::cout << "Heightmaps: " << mapa.GetHeightMapCount() << "\n";
        std::cout << "Objetos: " << mapa.GetObjectCount() << "\n";
        
        // Exportar para análise visual
        mapa.ExportHeightMapAsBMP("analise_heightmap_");
        mapa.AsASCIIFile(false);  // Gera FSMOut.txt
        
        mapa.Shutdown();
    }
    
    return 0;
}
```

### Exemplo 2: Modificação de Mapa

```cpp
#include "FSM.h"

int main() {
    Seraph::FSM mapa;
    
    if (mapa.Load("mapa_original.fsm")) {
        // Adicionar objetos decorativos
        mapa.ImportObject(100.0f, 0.0f, 100.0f, 0.0f, 1.0f, "Arvore01");
        mapa.ImportObject(150.0f, 0.0f, 120.0f, 1.57f, 0.8f, "Pedra01");
        
        // Salvar versão modificada
        mapa.Save("mapa_decorado.fsm");
        mapa.Shutdown();
    }
    
    return 0;
}
```

### Exemplo 3: Processamento de Pacotes

```cpp
#include "PKG.h"

int main() {
    Seraph::PKG gerenciador;
    
    // Extrair todos os arquivos do jogo
    std::cout << "Extraindo arquivos PKG...\n";
    gerenciador.Load(true);  // Descomprime
    
    std::cout << "Arquivos extraídos com sucesso!\n";
    return 0;
}
```

## Considerações Finais

A X-Legend Library representa um trabalho significativo de engenharia reversa para possibilitar a modificação de conteúdo de jogos X-Legend. Embora algumas funcionalidades ainda estejam em desenvolvimento ou sejam experimentais, a biblioteca oferece uma base sólida para:

- **Análise de Mapas**: Visualização e compreensão da estrutura de mapas
- **Modificação de Conteúdo**: Adição de objetos e alteração de terrenos
- **Ferramentas de Desenvolvimento**: Base para editores e utilitários

**Recomendações para Uso**:
1. Sempre faça backup dos arquivos originais
2. Teste modificações em ambiente controlado
3. Use funcionalidades experimentais (como PKG) com cautela
4. Contribua com melhorias e correções de bugs

**Contato**: Azazel - [RageZone Forum](https://forum.ragezone.com/members/2000318605.html)

---
*Esta documentação foi gerada através de análise do código fonte e pode conter informações baseadas em interpretação da implementação.*
