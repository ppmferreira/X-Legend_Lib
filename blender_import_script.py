"""
Script Python para Blender - Importar Coordenadas de Mapa X-Legend
Lê os arquivos TXT gerados pela biblioteca X-Legend_Lib e cria objetos no Blender

Uso:
1. Execute extract_coordinates_example.cpp para gerar os arquivos TXT
2. No Blender, execute este script no Text Editor
3. Os objetos serão criados nas coordenadas corretas
"""

import bpy
import bmesh
from mathutils import Vector
import os
from typing import Dict, List, Tuple

class XLegendMapImporter:
    def __init__(self):
        self.terrain_data = []
        self.object_data = []
        self.loaded_meshes: Dict[str, bpy.types.Mesh] = {}
        
    def clear_scene(self):
        """Remove todos os objetos da cena atual"""
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        print("🗑️ Cena limpa")
    
    def load_terrain_coordinates(self, filepath: str) -> bool:
        """Carrega coordenadas do terreno do arquivo TXT"""
        try:
            with open(filepath, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith('#') or not line:
                        continue
                    
                    parts = line.split(',')
                    if len(parts) == 4:
                        layer_id = int(parts[0])
                        x = float(parts[1])
                        y = float(parts[2])
                        height = float(parts[3])
                        
                        self.terrain_data.append({
                            'layer': layer_id,
                            'x': x,
                            'y': y,
                            'z': height
                        })
            
            print(f"✅ Carregados {len(self.terrain_data)} pontos de terreno")
            return True
            
        except FileNotFoundError:
            print(f"❌ Arquivo não encontrado: {filepath}")
            return False
        except Exception as e:
            print(f"❌ Erro ao carregar terreno: {e}")
            return False
    
    def load_object_coordinates(self, filepath: str) -> bool:
        """Carrega coordenadas dos objetos do arquivo TXT"""
        try:
            with open(filepath, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith('#') or not line:
                        continue
                    
                    parts = line.split(',')
                    if len(parts) == 6:
                        name = parts[0]
                        x = float(parts[1])
                        y = float(parts[2])
                        z = float(parts[3])
                        rotation = float(parts[4])
                        scale = float(parts[5])
                        
                        self.object_data.append({
                            'name': name,
                            'x': x,
                            'y': y,
                            'z': z,
                            'rotation': rotation,
                            'scale': scale
                        })
            
            print(f"✅ Carregados {len(self.object_data)} objetos")
            return True
            
        except FileNotFoundError:
            print(f"❌ Arquivo não encontrado: {filepath}")
            return False
        except Exception as e:
            print(f"❌ Erro ao carregar objetos: {e}")
            return False
    
    def create_terrain_mesh(self, layer_id: int = 0, sample_rate: int = 4):
        """Cria um mesh do terreno baseado nos pontos de altura"""
        print(f"🗺️ Criando terreno para layer {layer_id}...")
        
        # Filtrar pontos do layer especificado
        layer_points = [p for p in self.terrain_data if p['layer'] == layer_id]
        
        if not layer_points:
            print(f"❌ Nenhum ponto encontrado para layer {layer_id}")
            return
        
        # Determinar dimensões do grid
        max_x = max(p['x'] for p in layer_points)
        max_y = max(p['y'] for p in layer_points)
        
        # Criar mesh
        mesh = bpy.data.meshes.new(f"Terrain_Layer_{layer_id}")
        obj = bpy.data.objects.new(f"Terrain_Layer_{layer_id}", mesh)
        
        # Adicionar à cena
        bpy.context.collection.objects.link(obj)
        
        # Criar vertices (sampling para reduzir complexidade)
        vertices = []
        faces = []
        
        # Criar grid de vertices com sampling
        for i in range(0, int(max_x), sample_rate):
            for j in range(0, int(max_y), sample_rate):
                # Encontrar ponto de altura para esta coordenada
                height = 0.0
                for point in layer_points:
                    if abs(point['x'] - i) < sample_rate/2 and abs(point['y'] - j) < sample_rate/2:
                        height = point['z']
                        break
                
                # Converter coordenadas (Y e Z podem estar trocados no Blender)
                vertices.append((i, j, height))
        
        # Criar faces (opcional - para visualização do terreno)
        # Aqui você pode implementar triangulação se necessário
        
        mesh.from_pydata(vertices, [], faces)
        mesh.update()
        
        print(f"✅ Terreno criado com {len(vertices)} vertices")
    
    def create_placeholder_object(self, name: str, location: Tuple[float, float, float], 
                                rotation: float, scale: float) -> bpy.types.Object:
        """Cria um objeto placeholder (cubo) para representar objetos do mapa"""
        
        # Usar cache de meshes para objetos do mesmo tipo
        if name not in self.loaded_meshes:
            # Criar um cubo simples como placeholder
            bpy.ops.mesh.primitive_cube_add()
            placeholder = bpy.context.active_object
            placeholder.name = f"Placeholder_{name}"
            
            # Salvar mesh no cache
            self.loaded_meshes[name] = placeholder.data
            
        else:
            # Criar nova instância usando mesh cached
            mesh = self.loaded_meshes[name]
            placeholder = bpy.data.objects.new(f"Instance_{name}", mesh)
            bpy.context.collection.objects.link(placeholder)
        
        # Aplicar transformações
        placeholder.location = location
        placeholder.rotation_euler = (0, 0, rotation)  # Rotação em Z
        placeholder.scale = (scale, scale, scale)
        
        return placeholder
    
    def create_objects(self):
        """Cria todos os objetos do mapa"""
        print(f"🏠 Criando {len(self.object_data)} objetos...")
        
        created_objects = 0
        
        for obj_data in self.object_data:
            try:
                location = (obj_data['x'], obj_data['y'], obj_data['z'])
                
                placeholder = self.create_placeholder_object(
                    obj_data['name'],
                    location,
                    obj_data['rotation'],
                    obj_data['scale']
                )
                
                created_objects += 1
                
                # Mostrar progresso a cada 100 objetos
                if created_objects % 100 == 0:
                    print(f"   Criados {created_objects}/{len(self.object_data)} objetos...")
                    
            except Exception as e:
                print(f"❌ Erro ao criar objeto {obj_data['name']}: {e}")
        
        print(f"✅ {created_objects} objetos criados com sucesso")
    
    def import_map(self, terrain_file: str, objects_file: str, create_terrain: bool = True):
        """Importa mapa completo"""
        print("🚀 Iniciando importação de mapa X-Legend...")
        
        # Limpar cena
        self.clear_scene()
        
        # Carregar dados
        terrain_loaded = self.load_terrain_coordinates(terrain_file)
        objects_loaded = self.load_object_coordinates(objects_file)
        
        if not terrain_loaded and not objects_loaded:
            print("❌ Nenhum arquivo pôde ser carregado")
            return
        
        # Criar terreno se solicitado
        if create_terrain and terrain_loaded:
            self.create_terrain_mesh(layer_id=0, sample_rate=8)  # Amostragem para reduzir vértices
        
        # Criar objetos
        if objects_loaded:
            self.create_objects()
        
        print("🎉 Importação concluída!")

# Exemplo de uso
def main():
    # Caminhos dos arquivos (ajuste conforme necessário)
    terrain_file = "C:/Users/pedro/Desktop/GF ARKADIA/Map Editor/X-Legend_Lib/terrain_coordinates.txt"
    objects_file = "C:/Users/pedro/Desktop/GF ARKADIA/Map Editor/X-Legend_Lib/object_coordinates.txt"
    
    # Criar importador
    importer = XLegendMapImporter()
    
    # Importar mapa
    importer.import_map(terrain_file, objects_file, create_terrain=True)

# Executar se o script for rodado diretamente
if __name__ == "__main__":
    main()

"""
INSTRUÇÕES DE USO:

1. PREPARAÇÃO:
   - Compile e execute extract_coordinates_example.cpp
   - Certifique-se que os arquivos TXT foram gerados

2. NO BLENDER:
   - Abra o Text Editor
   - Cole este script
   - Ajuste os caminhos dos arquivos na função main()
   - Clique em "Run Script"

3. RESULTADO:
   - Terreno será criado como mesh com vertices nas alturas corretas
   - Objetos serão criados como cubos placeholder nas posições corretas
   - Use este resultado como base para substituir por modelos NIF reais

4. OTIMIZAÇÕES:
   - O script usa cache de meshes para objetos duplicados
   - Terreno é amostrado para reduzir complexidade
   - Progresso é mostrado durante a criação

5. PRÓXIMOS PASSOS:
   - Integrar com NifTools para carregar modelos reais
   - Implementar sistema de materiais
   - Adicionar suporte a múltiplas layers de terreno
"""
