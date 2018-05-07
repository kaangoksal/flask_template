from flaskapp import db, app
from datetime import datetime
# This is for UUID datatype....
from sqlalchemy.dialects.postgresql import UUID as DB_UUID

# This is for varchar datatype
from sqlalchemy import VARCHAR

# This is for timestamp datatype
from sqlalchemy import TIMESTAMP

# To be able to use sql functions
from sqlalchemy import func

from sqlalchemy import ForeignKey


class Device_dbModel(db.Model):

    __tablename__ = 'devices'
    example_id = db.Column(VARCHAR(60), primary_key=True)
    password = db.Column(VARCHAR(66), nullable=False)  # sha256 hash this shit
    device_name = db.Column(db.Text)
    owner = db.Column(VARCHAR(60), nullable=False)  # add not null default values
    type = db.Column(db.Text, nullable=False)
    sign_up_date = db.Column(TIMESTAMP(0), server_default=func.now())  # Add a default value to this guy
    last_ping = db.Column(TIMESTAMP(0), server_default=func.now())

    def __init__(self, example_id, password, owner, type):
        self.example_id = example_id
        self.password = password
        self.owner = owner
        self.type = type

    def __repr__(self):
        return str(self.type) + " Device with device_id " + str(self.device_id)

    @staticmethod
    def authenticate_device(auth):
        # TODO log authentication failures!
        if not auth:
            return False
        password = auth.password
        device_id = auth.username
        device_info = Device_dbModel.query.filter_by(device_id=device_id).first()
        if device_info is None:
            return False
        if device_info.password is not None:
            if device_info.password == password:
                # Update the device ping time
                device_info.last_ping = datetime.now()
                db.session.commit()
                return True
        return False

    @staticmethod
    def user_owns_device(user_id, device_id):
        """
        Checks whether the device is owned by the user
        :param user_id: user_id of the user that is requesting info from device
        :param device_id: the device that the info is being requested
        :return: true if the user owns the device, false if not
        """
        # TODO SQLInjection Protection
        # TODO Safety logging
        print("Checking for user ", user_id, " and device ", device_id)
        device_info = Device_dbModel.query.filter_by(device_id=device_id, owner=user_id).first()
        if device_info is None:
            #print("Device info was none! fuck!")
            return False
        elif device_info.owner == user_id and device_info.device_id == device_id:
            #print("Returned true! User owns the device")
            return True
        else:
            #print("shit did not fit here is the info ", device_info.owner, " dev_id ", device_info.device_id)
            return False
