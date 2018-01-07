import historio.client as client

app = None  # refer to Flask App in which we've already injected during application bootstrap
# Init Client through your bootstrap
client.historio(server='historio_server', port=5505, ignore_error=True, logger=app.logger)

model = None


class booking_controller(object):
    def post(self, request):  # FIRST EXAMPLE
        """Action where you create or Update Model
        _create_booking() returns a model. We can add historio decorator to handle that
        See it right below this function
        """
        model = self._create_booking(
            request=request)  # when _create_booking is invoked, historio Client will log model
        print('save me')

    @client.historio(user_id=get_current_user_id(), source='assignment', source_id=model.id)
    def _create_booking(self, request):
        return self.create_booking(request)
        # Magic is done right after this function execution

    def post_another_try(self, request):  # SECOND EXAMPLE
        """You can use historio client to push it manually"""
        model = self.create_booking(request)
        client.historio().push(model, get_current_user_id(), source='assignment', source_id=model.id)  # Magic happens
        # Magic is done

    def create_booking(self, request):
        """We prefer developer create another small function to handle your own model and return it right away"""
        model = AssignmentModelFromDynamo('assignment', 'params')

        model.save()

        return model

    def update_your_extend_model(self):  # THIRD EXAMPLE
        model = YourBookingModelSupporthistorio('extended_name', 'new description')
        model.update()
        client.historio().push(model, get_current_user_id())  # No need other parameters
        # Magic is done


def get_current_user_id():
    request = None  # It's just an example
    return request.user.id


class AssignmentModelFromDynamo(object):
    name = None
    description = None

    def __init__(self, name, description):
        self.description = description
        self.name = name

    def save(self):
        """
        Default save function which is supported through many different frameworks
        Returns:

        """
        print(self.name)
        print(self.description)


from historio import Model


# In order to handle this simpler, you can extend historio.Model
class YourBookingModelSupporthistorio(AssignmentModelFromDynamo, Model):
    def __init__(self, name, description):
        super(YourBookingModelSupporthistorio, self).__init__(name, description)

    def source(self):
        return 'booking'

    def get_data(self):
        return {'name': self.name, 'description': self.description}

    def source_id(self):
        return 'id_reflect_your_datasource'
