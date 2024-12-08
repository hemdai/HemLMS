<template>
  <div class="courses">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title">{{ course_detail.title }}</h1>
        <router-link 
        :to="{name: 'AuthorsView', params: { id: course_detail.account.id }}"
        class="subtitle"
        >
          By {{ course_detail.account.first_name + ' ' + course_detail.account.last_name }}</router-link>
      </div>
    </div>

    <section class="section">
      <div class="container">
        <div class="columns content">
          <div class="column is -2">
            <h2>Table Content</h2>
            <ul>
              <li v-for="lesson in lessons" v-bind:key="lesson.id">
                <a @click="setActiveLesson(lesson)">{{ lesson.title }}</a>
              </li>
            </ul>
          </div>

          <div class="column is-10">
            <template v-if="$store.state.user.isAuthenticated">
              <template v-if="activeLesson">
                <h2>{{ activeLesson.title }}</h2>
                <span class="tag is-warning" v-if="activity.status == 'started'" @click="trackDoneLesson">Started (Click to make Done)</span>
                <span class="tag is-success" v-if="activity.status == 'done'">Completed</span>

                {{ activeLesson.long_description }}
                <hr>
                <template v-if="activeLesson.lesson_type === 'quiz'">
                  <Quiz v-bind:quiz="quiz"></Quiz>
                </template>

                <template v-if="activeLesson.lesson_type === 'video'">
                  <VideoView v-bind:youtube_id="activeLesson.video_url"></VideoView>
                </template>

               <!-- Comment box start here   -->
               <template v-else-if="activeLesson.lesson_type === 'article' "> 
                <CourseComment 
                  class="media box"
                  v-for="comment in comments"
                  v-bind:key="comment.id"
                  v-bind:comment="comment"
                  >
                  <div class="media-content">
                    <div class="content">
                      <p>
                        <strong>{{ comment.name }}</strong> - {{ comment.created_at }}
                        <br>
                        {{ comment.content }}
                      </p>
                    </div>
                    </div>

                </CourseComment>
                <AddComments v-bind:course="course_detail"
                v-bind:active-lesson="activeLesson"
                v-on:submitComment="submitComment">
                </AddComments>
              </template>
              <!-- fin du comment box -->
              </template v-else>
              {{ course_detail.long_description }}
            </template>
            <template v-else>
              <h2>Not Authenticated</h2>
              <p>
                You are not authenticated. Please log in to view this content.
              </p>
            </template>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import CourseComment from "@/components/CourseComment.vue";
import AddComments from "@/components/AddComments.vue";
import Quiz from "@/components/Quiz.vue";
import VideoView from "@/components/VideoView.vue";
import axios from "axios";
export default {
  components: {
    CourseComment,
    AddComments,
    Quiz,
    VideoView
  },
  data() {
    return {
      course_detail: {
        account: {
          first_name: "",
          last_name: "",
          id: 0,
        }
      },
      lessons: [],
      comments: [],
      activeLesson: null,
      errors: [],
      quiz: {},
      activity: {},
      comment: {
        name: "",
        content: "",
      }
    };
  },
  async mounted() {
    const slug = this.$route.params.slug;
    await axios
      .get(`courses/${slug}`)
      .then((response) => {
        console.log(response.data, "the course Detail");
        this.course_detail = response.data.course_detail;
        this.lessons = response.data.lessons;
      })
      .catch((error) => {
        console.log(error);
      });
      document.title = this.course_detail.title + " -LMS";
  },
  methods: {
    submitComment(comment) {
      this.comments.push(comment);
    },
     setActiveLesson(lesson) {
       this.activeLesson = lesson
       console.log(lesson.lesson_type, "the Lesson type");
       if (lesson.lesson_type == "quiz") {
         this.getQuiz()
      
    } else {
      this.getComments();
    }
    this.trackStartedLesson();
    },
    trackStartedLesson() {
      axios
        .post(`/activity/track-started/${this.$route.params.slug}/${this.activeLesson.slug}/`)
        .then((response) => {
          this.activity = response.data
        })
        .catch((error) => {
          console.log(error);
        });
    },
     trackDoneLesson() {
      axios
        .post(`/activity/track-completed/${this.$route.params.slug}/${this.activeLesson.slug}/`)
        .then((response) => {
          this.activity = response.data
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getQuiz() {
      axios
        .get(`/quizes/${this.course_detail.slug}/${this.activeLesson.slug}`)
        .then((response) => {
          if (response.data.length == 0) {
            return
          }
          this.quiz = response.data[0];
          this.selectedAnswer = "";
        })
        .catch((error) => {
          console.log(error);
        })
    },
  getComments() {
    axios
      .get(`/courses/${this.course_detail.slug}/${this.activeLesson.slug}/comments`)
      .then((response) => {
        console.log("the comments",response.data);
        this.comments = response.data;
      })
      .catch((error) => {
        console.log(error);
      });
  }
  },
}
</script>
