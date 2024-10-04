import courier

from courier.client import Courier

client = Courier(authorization_token="pk_prod_6DRTMXQ27JMRS4HGHHCCZ8C3MJJK")

response = client.send(
    message=courier.TemplateMessage(
      template="FFM4ESSW9E49B5H73MXVG0HKQ5WA",
      to=courier.UserRecipient(
        email="C_Rebello18@cranford.hounslow.sch.uk",
        data={
          "code": f"{code}",
          "user": f"{user}",
          "verification_code": f"{code}",
          "expiry_time": f"{expiry_time}",
        }
      ),
    )
)
print(response.request_id)
