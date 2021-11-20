# import translators
# import numpy as np
# import cv2
# from PIL import Image
# from rudalle.pipelines import generate_images, show, super_resolution, cherry_pick_by_clip
# from rudalle import get_rudalle_model, get_tokenizer, get_vae, get_realesrgan, get_ruclip
# from rudalle.utils import seed_everything
# import io
# device = 'cuda'
# dalle = get_rudalle_model('Malevich', pretrained=True, fp16=True, device=device)
#
# #кстати да, картинку стоит superresизть перед отправкой, но вы
# realesrgan = get_realesrgan('x2', device=device) # x2/x4/x8
# tokenizer = get_tokenizer()
#
# vae = get_vae(dwt=True).to(device)  # for stable generations you should use dwt=False
# ruclip, ruclip_processor = get_ruclip('ruclip-vit-base-patch32-v5')
# ruclip = ruclip.to(device)
#
#
#
# seed_everything(42)
#
#
# def generate(message: str):
#     top_p = 0.95
#     top_k = 2000
#     images_num = 1
#     req, sc = generate_images(message, tokenizer, dalle, vae, top_k=top_k, images_num=images_num, top_p=top_p)
#
#     cv2img = np.array(req[0].convert('RGB'))
#
#     res, im_png = cv2.imencode(".png", cv2img)
#
#     return io.BytesIO(im_png.tobytes())