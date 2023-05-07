from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from home.models import CustomModel
from django.core.exceptions import PermissionDenied
from django.template.loader import render_to_string




class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:
            id = request.user.id
            check_user = User.objects.get(id=id)
            user = check_user.is_superuser
            if not user:
                try:
                    checkuser = CustomModel.objects.get(user_id=id)
                    key = checkuser.is_pass_change
                    if key == True:
                        messages.warning(request, 'Your account has been suspended.')
                        print(messages.warning)
                        return render(request, 'login.html', {'warning': messages.warning})
                        # raise PermissionDenied('Your account has been suspended')

                except CustomModel.DoesNotExist:
                    checkuser = CustomModel.objects.create(user_id=id, is_pass_change=False)

            response = self.get_response(request)
        else:
            response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, PermissionDenied):

            error_message = 'Your account has been suspended.'
            error_html = render_to_string('error.html', {'error_message': error_message})

            return HttpResponse(error_html)






# class CustomMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
        # if request.user.is_authenticated:
        #     id =  request.user.id
        #     check_user = User.objects.get(id = id)
        #     user = check_user.is_superuser
        #     if user == False:
        #         checkuser = CustomModel.objects.get(user_id = id)
        #         if checkuser:
        #             print('=======>', checkuser.is_pass_change )
        #             key = checkuser.is_pass_change
        #             if key == True:
        #                 print('<=======>')
        #                 messages.warning(request, 'Your account has been suspended.')
        #                 raise PermissionDenied('Your Account has been suspended')
        #         else:
        #             checkuser = CustomModel.objects.create(user_id = id, is_pass_change=False)
        #             checkuser.save()
        #     response = self.get_response(request)

        # else:
        #     response = self.get_response(request)
        # return response

# class CustomMiddleware:
    # def __init__(self, get_response):
    #     self.get_response = get_response

    # def __call__(self, request):

    #     if request.user.is_authenticated:
    #         id =  request.user.id
    #         check_user = User.objects.get(id = id)
    #         user = check_user.is_superuser
    #         print(user)
    #         if user == False:
    #             checkuser = CustomModel.objects.get(user_id = id)
    #             key = checkuser.is_pass_change
    #             if key == False:
    #                 is_pass_change=True
    #                 CustomModel.objects.filter(user_id=id).update(is_pass_change=is_pass_change)
    #                 response = self.get_response(request)
    #             else:
    #                 response = logout(request)
    #         response = self.get_response(request)
    #     else:
    #         response = self.get_response(request)
    #     return response



