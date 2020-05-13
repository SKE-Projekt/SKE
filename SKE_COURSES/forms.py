from django import forms


class CoursePackageForm(forms.Form):
    course_package_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super(CoursePackageForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'file-input is-primary'
