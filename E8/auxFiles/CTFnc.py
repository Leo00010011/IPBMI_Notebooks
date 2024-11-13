import numpy as np
try:
    from auxFiles.auxFnc import *
except:
    from auxFnc import *

def source(Kpv, I0):
  N0 = I0
  eE = Kpv * 0.4
  return N0, eE

def cube_phantom_cc(edge_size, energy):
    soft_coef = round(get_coef(index=4, energy=energy), 2)
    bone_coef = round(get_coef(index=2, energy=energy), 2)
    air_coef = round(get_coef(index=1, energy=energy), 2)
    print(soft_coef, bone_coef)

    air_size = edge_size * 2
    if edge_size > 2 and np.log2(edge_size) % 1 == 0:
        soft_tissue_size = edge_size
        bone_size = int(edge_size / 2)
        tissue = np.zeros(
            (soft_tissue_size, soft_tissue_size, soft_tissue_size))
        tissue[:] = soft_coef
        offset = int((soft_tissue_size - bone_size) / 2)
        tissue[offset:offset + bone_size, offset: offset + bone_size, offset:offset+bone_size] = bone_coef
        # tissue = np.full((air_size, air_size, air_size), air_coef)
        # offset_soft = int((air_size / 2) - (edge_size / 2))
        # tissue[offset_soft:offset_soft + edge_size, offset_soft: offset_soft + edge_size, offset_soft:offset_soft + edge_size] = soft_coef
        
        # bone_size = int(edge_size / 2)

        # offset_bone = int((air_size - bone_size) / 2)
        # tissue[offset_bone:offset_bone + bone_size, offset_bone: offset_bone + bone_size, offset_bone:offset_bone + bone_size] = bone_coef
        return tissue
    else:
        print('not powers of 2')
        return

def interactor_CT(N0, obj, zPos, nProjections):
  slice = obj[:, zPos, :]
  angles = np.linspace(0, 360, nProjections, endpoint=False)
  sinograma = np.zeros((nProjections, slice.shape[1]))
  img = Image.fromarray(slice)
  for i, angle in enumerate(angles):
    rotated_img = img.rotate(angle)
    projection_coef = np.sum(rotated_img, axis=0)
    projection = N0 * np.exp(-projection_coef / projection_coef.shape[0])
    sinograma[i, :] = projection

  return sinograma

def detectSinogram(qImage, nProjections, nDetectors):
  detected_img = np.zeros((nProjections, nDetectors))
  for i in range(nProjections):
    line = detector_1D(qImage, i, nDetectors)
    detected_img[i, :] = line
  return detected_img

def detector_1D(qImage, angle, nDetectors):
  detected_line = np.full(nDetectors, 75000)
  start = nDetectors // 2 - qImage.shape[1] // 2
  end = nDetectors // 2 + qImage.shape[1] // 2
  detected_line[start:end] = qImage[angle, :]
  return detected_line

def process_CT(image, N0):
    compensated_sinogram = -np.log(image / N0)
    return compensated_sinogram

def reconstructor(sinogram, nProj):
    rows, columns = sinogram.shape
    reconstructed_image = np.zeros((columns, columns))
    
    angles = np.linspace(0, 360, rows, endpoint=False)
    if nProj < rows:
        space = rows // nProj
        projections = sinogram[::space]
        angles = angles[::space]
    else:
        projections = sinogram
    
    for i, angle in enumerate(angles):
        projection = projections[i]
        projection_img = np.tile(projection, (columns, 1))
        projection_pil = Image.fromarray((projection_img * 255).astype(np.uint8))
        rotated_projection = projection_pil.rotate(angle)
        rotated_projection_np = np.array(rotated_projection)/255
        reconstructed_image += rotated_projection_np
    reconstructed_image = reconstructed_image / angles.shape[0]
    return reconstructed_image

def setHounsfield(Image, eE):
    water_coef = get_coef(5,eE)
    return ((Image - water_coef)/water_coef)*1000

def displayWL(Image, W, L, maxGL):
    min_intensity = L - W/2
    Image = (Image - min_intensity)/W
    Image[Image < 0] = 0
    Image[Image > 1] = 1
    Image = Image*maxGL
    return Image
