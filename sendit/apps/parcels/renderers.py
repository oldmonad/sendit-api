import json

from rest_framework import renderers


class ParcelDeliveryJsonRenderer(renderers.BaseRenderer):
    """
    This class determines the display format
    for the parcels and any errors
    """

    media_type = "application/json"
    format = "json"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, list):
            return json.dumps({"parcels": data, "parcel_count": len(data)})
        else:
            error = data.get("detail")
            if error:
                return json.dumps({"message": data})
            return json.dumps({"parcel": data})
