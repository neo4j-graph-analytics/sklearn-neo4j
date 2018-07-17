import importlib

import numpy as np


class ModelPersistence:
    def __init__(self, driver):
        self.driver = driver

    save_model_procedure_query = """\
    CALL sklearn.model.save(
        $modelName, $module, $class, $fields
    )
    """

    def save(self, model, name, fields):
        params = {
            "modelName": name,
            "module": model.__module__,
            "class": model.__class__.__name__,
            "fields": {}
        }
        attrs = params["fields"]
        for field in fields:
            raw_value = getattr(model, field)
            coerced_value = raw_value

            if isinstance(raw_value, np.ndarray):
                coerced_value = raw_value.tobytes()

            data_type = "{0}.{1}".format(type(raw_value).__module__, type(raw_value).__name__)

            attrs[field] = {
                "value": coerced_value,
                "type": data_type
            }

            if data_type == "numpy.ndarray":
                attrs[field]["dataType"] = raw_value.dtype.name
                attrs[field]["shape"] = list(raw_value.shape)

        with self.driver.session() as session:
            session.run(self.save_model_procedure_query, params)

    load_model_query = """\
    call sklearn.model.load($modelName)        
    """

    def load(self, name):
        with self.driver.session() as session:
            result = session.run(self.load_model_query, {"modelName": name})
            only_row = result.peek()
            model = only_row["model"]
            fields = only_row["fields"]

        ModelClass = getattr(importlib.import_module(model["module"]), model["class"])
        instance = ModelClass()
        for field in fields:
            if field["type"] == "numpy.ndarray":
                value = np.frombuffer(field["value"], dtype=field["dataType"]).reshape(tuple(field["shape"]))
            else:
                value = field["value"]
            setattr(instance, field["key"], value)
        return instance
