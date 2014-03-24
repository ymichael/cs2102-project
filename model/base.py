class BaseModel(object):
    """An abstract model class.

    Provides common interface for models for:
    - Accessing properties
    - REST conventions (GET, POST, PUT)
    """
    # Properties of the Model
    properties = []

    def info(self):
        if hasattr(self, '_info'):
            return self._info

        if self.check_is_saved():
            self.hard_get()
        else:
            self._info = {}
        
        return self._info

    def hard_get(self):
        self._info = self.get() or {}

    def check_is_saved(self):
        """Returns True if model has been saved to the db before."""
        raise NotImplementedError()

    def get(self):
        """Returns dictionary object from the database.

        Corresponds to GET request."""
        raise NotImplementedError()


    def validate(self):
        """Returns True if model passes validation.

        Expected to be overriden in subclasses.
        """
        raise NotImplementedError()

    def post(self):
        """Creates new object in the database.

        Corresponds to POST request."""
        raise NotImplementedError()

    def put(self):
        """Updates existing object in the database.

        Corresponds to PUT request."""
        raise NotImplementedError()

    def save(self):
        if not self.validate():
            raise Exception('Trying to save invalid Model.')
        if self.check_is_saved():
            retval = self.put()
        else:
            retval = self.post()

        # Update self._info object.
        self.hard_get()
        return retval

    def set_prop(self, attr, val):
        self.info()[attr] = val

    def get_prop(self, attr):
        return self.info().get(attr)

    def __getattr__(self, attr):
        if attr in self.properties:
            return self.get_prop(attr)
        else:
            # Default behaviour
            raise AttributeError

    def __setattr__(self, attr, val):
        if attr in self.properties:
            self.set_prop(attr, val)
        else:
            super(BaseModel, self).__setattr__(attr, val)