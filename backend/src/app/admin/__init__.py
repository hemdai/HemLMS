from .register_admin import AdminSite, registry
from src.models import (
    Course,
    LessonModel,
    Category,
    Account,
    CommentModel,
    QuizModel,
)
from src.schemas import (
    CourseSchema,
    LessonSchema,
    CategorySchema,
    AccountSchema,
    CommentSchema,
    QuizeSchema,
)
from src.app.activity.model import ActivityModel
from src.app.activity.schemas import ActivitySchema

AdminSite.register_admin(Course, CourseSchema)
AdminSite.register_admin(LessonModel, LessonSchema)
AdminSite.register_admin(Category, CategorySchema)
AdminSite.register_admin(ActivityModel, ActivitySchema)
AdminSite.register_admin(Account, AccountSchema)
AdminSite.register_admin(CommentModel, CommentSchema)
AdminSite.register_admin(QuizModel, QuizeSchema)
