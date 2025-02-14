from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View


class BaseFormView(LoginRequiredMixin, View):
    model = None
    form_class = None
    template_name = None
    success_url = None
    title_add = None
    title_edit = None

    def get_object(self):
        object_id = self.kwargs.get("id", None)
        return get_object_or_404(self.model, id=object_id) if object_id else None

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj is None:
            title = self.title_add
            button_delete = False
        else:
            title = self.title_edit
            button_delete = True

        form = self.form_class(instance=obj)
        context = {
            "form": form,
            "object": obj,
            "title": title,
            "button_delete": button_delete,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        action = request.POST.get("action")
        form = self.form_class(data=request.POST, instance=obj)

        if action == "post":
            if form.is_valid():
                form.save()
                return redirect(self.success_url)

        if action == "delete":
            obj.delete()
            return redirect(self.success_url)

        context = {
            "form": form,
            "object": obj,
        }
        return render(request, self.template_name, context)
