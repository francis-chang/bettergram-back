from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from cloudinary.utils import cloudinary_url
from cloudinary.uploader import upload
from flask import request
from models.image import  ImageModel


class Image(Resource):
    @jwt_required
    @classmethod
    def post(cls):
        caption = request.form.to_dict()["caption"]
        image = request.files["image"]

        if image:
            uploaded_image = upload(image)
            image_sizes = ImageModel.find_dimensions(image)
            width = image_sizes[0]
            height = image_sizes[1]

            if width / height > 1.6:
                width = 700
                height = round(700 * image_sizes[1] / image_sizes[0])

                url = cloudinary_url(
                    uploaded_image["public_id"],
                    transformation = [
                        {"width": 700, "height": height},
                        {"crop": "crop", "width": 450, "x": 125, "height": height},
                        {"format": "jpg", "width": 450, "height": height, "quality": "auto: good"}
                    ]

                )[0]
                is_long = True
            else:
                width = 450
                height = round(450 * image_sizes[1] / image_sizes[0])
                url = cloudinary_url(
                    uploaded_image["public_id"],
                    format="jpg",
                    width=450,
                    quality="auto:good"
                )[0]
                is_long = False

            full_size_url = cloudinary_url(uploaded_image["public_id"], format="jpg")[0]
            user_id = get_jwt_identity()
            image_obj = ImageModel(
                caption=caption,
                url=url,
                full_size_url=full_size_url,
                width=width,
                height=height,
                is_long=is_long,
                user_id = user_id
            )

            try:
                image_obj.save_to_db()
            except:
                return {"message": "error uploading file"}, 500
            return image_obj.json(), 201
        return {"message": "Please select an image"}, 401

