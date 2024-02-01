import os
import shutil

from selenium import webdriver
from selenium.webdriver.common.by import By

from django.urls import reverse
from django.conf import settings

from quiz import models as quiz_models


def capture_screenshot(quiz_uuid):
    # get all instances
    quiz_instances = quiz_models.QuizData.objects.filter(quiz_uuid=quiz_uuid).all()

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    try:

        # urls = []
        # file_names = []
        for instance in quiz_instances:
            # window size
            driver.set_window_size(1920, 1080)

            # prepare url
            url = reverse("image-api", kwargs={"question_uuid": instance.question_uuid})

            # add domain with url
            new_url = "http://127.0.0.1:8000" + url

            # prepare url in the driver
            driver.get(new_url)

            # for testing browser stay 20 sec
            # time.sleep(20)

            # find element from the html page
            element = driver.find_element(By.CLASS_NAME, "square")

            # save image
            element.screenshot(f"question_{instance.question_uuid}.png")

            source_path = f"question_{instance.question_uuid}.png"
            destination_path = os.path.join(
                settings.MEDIA_ROOT, f"question_{instance.question_uuid}.png"
            )

            shutil.move(source_path, destination_path)

            # ====================== start
            # print(destination_path)
            # image_object = default_storage.open(destination_path, 'rb')

            # print("image_object", image_object)
            # response = HttpResponse(image_object.read(), content_type='image/png')
            # response['Content-Disposition'] = 'attachment; filename=question_%s.png' % instance.question_uuid
            # return response

            # ====================== end

            # # Find File in static directory
            # image_file = finders.find(f"question_{instance.question_uuid}.png", )

            # print("image_file",image_file)

            # if not image_file:
            #     print("Error...!")

            # try:
            #     with open(image_file, "rb") as fh:
            #         response = HttpResponse(
            #             fh.read(),
            #             content_type="application/png",
            #         )
            #         response[
            #             "Content-Disposition"
            #         ] = "inline; filename='question_{instance.question_uuid}.png'"
            #         return response
            # except Exception as e:
            #     print("Error", e)

            # remove image
            # os.remove(f"./static/question_{instance.question_uuid}.png")

    finally:
        driver.quit()
