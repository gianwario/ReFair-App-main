<template>
  <div class="container">
    <div class="row">
      <div>
        <h1>ReFair App</h1>
        <!-- Contenuto Capitolo 1 -->
        <div class="content">
          <!-- Il contenuto principale rimane lo stesso -->

          <div id="chapter1">
            <ChapterTitle chapterTitle="ReFair in a nutshell" />

            <ParagraphTitle paragraphTitle="What is ReFair?" />

            <div class="paragraph_content">
              ReFair is an
              <strong>innovative context-aware automated framework</strong>
              designed to support fairness requirements engineering. It utilizes
              natural language processing (NLP) and word embedding techniques to
              identify sensitive features in user stories (USs), alerting
              developers early on to potential concerns.
            </div>

            <ParagraphTitle paragraphTitle="Main functionalities" />

            <div class="paragraph_content">
              ReFair is a model that consists of two main components:
              <ul>
                <li>
                  <strong> Application Domain Classification. </strong> This
                  component is responsible for classifying the most likely
                  application domain of the US among the 34 domains available in
                  the ontology;
                </li>
                <li>
                  <strong> Machine Learning Tasks Classification. </strong> This
                  is responsible for classifying the ML tasks likely to be
                  employed when imple menting the US. The problem has been
                  modeled as a multi-label classification task, as a US may be
                  operationalized using multiple ML techniques;
                </li>
                <li>
                  <strong> Sensitive Features Recommendation. </strong> The
                  application domain and ML tasks classified in the previous
                  step are finally used to recommend sensitive features. ReFair
                  exploits the base ontology to identify the sensitive features
                  connected to both the application domain and ML tasks
                  concerned with the the classified domain. The intersection of
                  those sensitive features represents the final outcome of the
                  framework. In other terms the outcome comprises the set of
                  sensitive features relevant when jointly con sidering the
                  application domain and the learning tasks.
                </li>
              </ul>
            </div>

            <ParagraphTitle paragraphTitle="Technical aspects" />

            <div class="paragraph_content">
              The framework has been designed to be conservative enough and
              identify all the potential ML tasks that may lead to unfairness.
              From a practical perspective, this choice may allow the users to
              receive a larger set of sensitive features, hence
              <strong> favoring recall over precision</strong>.
            </div>
          </div>

          <br /><br />
          <!-- Contenuto Capitolo 2 -->
          <div id="chapter2">
            <ChapterTitle chapterTitle="How to use ReFair" />

            <ParagraphTitle paragraphTitle="Recommendation" />

            <div class="paragraph_content">
              To properly run the ReFair analysis, you should upload a file that
              meets specific conditions:
              <ul>
                <li>The file should be in <strong>xlsx format</strong>;</li>
                <li>
                  The spreadsheet can contain an arbitrary number of columns,
                  but at least
                  <strong>one column should be named "User Story"</strong> and
                  should contain all the User Stories you want to be analyzed.
                </li>
              </ul>
            </div>

            <ParagraphTitle paragraphTitle="Web-app functionalities" />

            <div class="paragraph_content">
              In detail:
              <ul>
                <li>
                  The <strong> Select </strong> Button allows you to select a
                  User Stories spreadsheet from your machine;
                </li>
                <li>
                  The <strong> Load </strong> Button allows you to upload the
                  User Stories spreadsheet;
                </li>
                <li>
                  The <strong> Download all </strong> Button allows you to
                  download a structured JSON report containing the results for
                  all the User Stories analyzed by ReFair;
                </li>
                <li>
                  The
                  <strong> Analyze </strong> Button allows you to visualize the
                  ReFair analysis for a single User Story.
                </li>
                <li>
                  The <strong> Download </strong> Button (in the pop-up window)
                  allows you to download a structured JSON report containing the
                  results of the single User Story analyzed by ReFair;
                </li>
                <li>
                  The <strong> Close </strong> Button simply closes the pop-up
                  window.
                </li>
              </ul>
            </div>
          </div>

          <br /><br />

          <!-- Contenuto Capitolo 3 -->
          <div id="chapter3">
            <ChapterTitle chapterTitle="ReFair framework" />

            <div
              class="btn-toolbar mb-3 justify-content-between"
              role="toolbar"
              aria-label="Toolbar with button groups"
            >
              <div class="file-upload">
                <input
                  type="file"
                  id="file"
                  class="form-control"
                  @change="handleStoriesUpload($event)"
                />

                <!---->

                <SelectButton
                  buttonType="button"
                  labelFor="file"
                  labelClass="button__text"
                  labelText="Select file"
                />

                <!--<button type="button" class="button select">
                  <span class="button__icon"
                    ><label for="file" class="button__text"> Select file </label><ion-icon name="document-attach-outline"></ion-icon
                  ></span>
                </button>-->
                <!---->
                <span id="file-name" class="file-name">No file selected</span>
              </div>
              <div>
                <button
                  v-on:click="submitFile()"
                  type="button"
                  class="button load"
                  style="margin-right: 20px"
                >
                  <span class="button__text">Load</span>
                  <span class="button__icon"
                    ><ion-icon name="cloud-upload-outline"></ion-icon
                  ></span>
                </button>
                <button
                  v-on:click="reportStories()"
                  type="button"
                  class="button report"
                  id="report"
                >
                  <span class="button__text">Download all</span>
                  <span class="button__icon"
                    ><ion-icon name="code-slash-outline"></ion-icon
                  ></span>
                </button>
              </div>
            </div>

            <table class="table table-hover">
              <thead>
                <tr>
                  <th scope="col">
                    <ParagraphTitle paragraphTitle="User Stories" />
                  </th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(story, index) in paginatedStories" :key="index">
                  <td>{{ story }}</td>
                  <td>
                    <div>
                      <button
                        type="button"
                        class="button analyze"
                        @click="toggleAnalyzeStoryModal(story)"
                      >
                        <span class="button__text">Analyze</span>
                        <span class="button__icon">
                          <ion-icon name="analytics-outline"></ion-icon>
                        </span>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>

            <!-- Controlli di Paginazione -->
            <div v-if="fileLoaded" class="pagination">
              <button
                @click="changePage(currentPage - 1)"
                :disabled="currentPage === 1"
              >
                Previous
              </button>

              <!-- Input per inserire il numero di pagina -->
              <input
                type="number"
                v-model.number="currentPageInput"
                @change="changePage(currentPageInput)"
                :min="1"
                :max="totalPages"
              />

              <!-- Mostra le pagine -->
              <span v-if="currentPage > 2">1,</span>
              <span v-if="currentPage > 3">...,</span>
              <span v-if="currentPage > 1">{{ currentPage - 1 }},</span>
              <span>{{ currentPage }},</span>
              <span v-if="currentPage < totalPages"
                >{{ currentPage + 1 }},</span
              >
              <span v-if="currentPage < totalPages - 2">...,</span>
              <span v-if="currentPage < totalPages - 1">{{ totalPages }}</span>

              <button
                @click="changePage(currentPage + 1)"
                :disabled="currentPage === totalPages"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Capitoli di navigazione -->

    <div class="sidebar">
      <p class="title_sidebar">ON THIS PAGE</p>
      <div
        class="indicator"
        :style="{ transform: `translateY(${indicatorPosition}px)` }"
      ></div>
      <ChapterButton
        btnClass="btn_chapter"
        dataChapter="chapter1"
        buttonText="ReFair in a nutshell"
        chapterId="chapter1"
        @scrollToChapter="scrollToChapter"
      />
      <ChapterButton
        btnClass="btn_chapter"
        dataChapter="chapter2"
        buttonText="How to use ReFair"
        chapterId="chapter2"
        @scrollToChapter="scrollToChapter"
      />
      <ChapterButton
        btnClass="btn_chapter"
        dataChapter="chapter3"
        buttonText="ReFair framework"
        chapterId="chapter3"
        @scrollToChapter="scrollToChapter"
      />
    </div>

    <!-- analyze Story Modal -->
    <div
      ref="analyzeStoryModal"
      class="modal fade"
      :class="{
        show: activeAnalyzeStoryModal,
        'd-block': activeAnalyzeStoryModal,
      }"
      tabindex="-1"
      role="dialog"
    >
      <div class="modal-dialog modal-xl" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Story Details</h5>
            <div>
              <button
                type="button"
                class="button close"
                data-dismiss="modal"
                @click="closeAnalyzeStoryModal"
                style="margin-right: 10px"
              >
                <span class="button__text">Close</span>
                <span class="button__icon"
                  ><ion-icon name="close-circle-outline"></ion-icon
                ></span>
              </button>
            </div>
          </div>
          <div class="modal-body">
            <p class="pt-3 mx-4"><b>User Story: </b> {{ story }}</p>
            <p class="pt-3 mx-4"><b>Story Domain: </b> {{ story_domain }}</p>
            <div class="pt-3 mx-4">
              <b>Story Tasks</b>
              <hr />
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th scope="col">Task</th>
                    <th scope="col">Sensitive Features</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(features, task) in story_tasks" :key="task">
                    <td>{{ task }}</td>
                    <td>
                      {{ features.toString().replaceAll(",", " - ") }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div
              v-if="
                series[0]['data'].length != null &&
                series[0]['data'].length > 0 != []
              "
              class="pt-3 mx-4"
            >
              <apexchart
                width="1000"
                type="bar"
                :options="options"
                :series="series"
                style="color: #212223; background-color: white"
              ></apexchart>
            </div>
            <div v-else class="pt-3 mx-4">No sensitive features suggested</div>
          </div>
          <div class="modal-footer">
            <button
              v-on:click="reportStory()"
              type="button"
              class="button report"
              id="report"
            >
              <span class="button__text">Download</span>
              <span class="button__icon"
                ><ion-icon name="code-slash-outline"></ion-icon
              ></span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="activeAnalyzeStoryModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<script>
import axios from "axios";
import downloadjs from "downloadjs";
import VueApexCharts from "vue-apexcharts";

import ChapterButton from "./ChapterButton.vue";
import ChapterTitle from "./ChapterTitle.vue";
import ParagraphTitle from "./ParagraphTitle.vue";
import SelectButton from "./SelectButton.vue";

const server = "http://localhost:5001";

export default {
  components: {
    ChapterButton,
    ChapterTitle,
    ParagraphTitle,
    SelectButton,
  },
  data() {
    return {
      activeAnalyzeStoryModal: false,
      story: "",
      story_domain: "",
      story_tasks: [],
      stories: [],
      file: "",
      options: {
        chart: {
          id: "vuechart-example",
        },
        xaxis: {
          categories: [],
        },
      },
      series: [
        {
          name: "series-1",
          data: [],
        },
      ],
      activeButton: null, // Nuova proprietà per tracciare il pulsante attivo
      indicatorPosition: 0, // Posizione della linea
      currentPage: 1, // Pagina corrente
      storiesPerPage: 30, // Numero di user stories per pagina
      fileLoaded: false, // Variabile per tracciare se un file è stato caricato
      currentPageInput: 1, // Variabile per tracciare l'input dell'utente per il numero di pagina
    };
  },
  methods: {
    handleStoriesUpload(event) {
      this.file = event.target.files[0];
    },

    reportStories() {
      let formData = new FormData();
      console.log(this.stories);
      formData.append("stories", JSON.stringify(this.stories));

      axios
        .post(server + "/reportStories", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          console.log(res.data);
          downloadjs(
            ("" + res.data).replaceAll("'", '"'),
            "report.json",
            "application/json"
          );
        })
        .catch((error) => {
          console.log(error);
        });
    },

    reportStory() {
      let formData = new FormData();
      console.log(this.story);
      formData.append("story", JSON.stringify(this.story));

      axios
        .post(server + "/reportStory", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          console.log(res.data);
          downloadjs(
            ("" + res.data).replaceAll("'", '"'),
            "report-" + this.story + ".json",
            "application/json"
          );
        })
        .catch((error) => {
          console.log(error);
        });
    },

    submitFile() {
      let formData = new FormData();
      formData.append("stories", this.file);

      axios
        .post(server + "/storiesload", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          if (typeof res.data.stories === "undefined") {
            alert(res.data.motivation);
            this.stories = [];
            this.fileLoaded = false; // Imposta false se il caricamento fallisce
          } else {
            const reportBtn = document.querySelector("#report");
            reportBtn.classList.remove("disabled");
            this.stories = res.data.stories;
            this.currentPage = 1; // Resetta la pagina corrente dopo il caricamento
            this.fileLoaded = true; // Imposta true se il caricamento ha successo
          }
        })
        .catch(() => {
          this.stories = [];
          this.fileLoaded = false; // Imposta false se il caricamento fallisce
        });
    },

    toggleAnalyzeStoryModal(story) {
      if (story) {
        this.story = story;
        let formData = new FormData();
        formData.append("story", this.story);

        axios
          .post(server + "/analyzeStory", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then((res) => {
            this.story_domain = res.data.domain;
            this.story_tasks = res.data.tasks_features;

            console.log(this.story_tasks);
            const body = document.querySelector("body");
            this.activeAnalyzeStoryModal = !this.activeAnalyzeStoryModal;

            var data = [];

            Object.keys(res.data.features_counts).forEach(function (key) {
              data.push({
                x: key,
                y: [res.data.features_counts[key]],
              });
            });

            if (this.activeAnalyzeStoryModal) {
              this.series = [
                {
                  name: "occurrencies",
                  data: data,
                },
              ];
              console.log(this.series[0]["data"]);
              body.classList.add("modal-open");
            } else {
              body.classList.remove("modal-open");
            }
          })
          .catch((error) => {
            console.error(error);
          });
      }
    },

    // Pagination
    changePage(page) {
      if (page > 0 && page <= this.totalPages) {
        this.currentPage = page;
        this.currentPageInput = page; // Aggiorna l'input della pagina corrente
      }
    },

    // Capitoli
    scrollToChapter(chapterId) {
      const button = this.$el.querySelector(`[data-chapter="${chapterId}"]`);
      this.activeButton = button; // Aggiorna il pulsante attivo
      this.updateIndicator(); // Aggiorna la posizione dell'indicatore

      document.getElementById(chapterId).scrollIntoView({ behavior: "smooth" });
    },

    updateIndicator() {
      if (!this.activeButton) return;
      const buttonRect = this.activeButton.getBoundingClientRect();
      const sidebarRect = this.$el
        .querySelector(".sidebar")
        .getBoundingClientRect();
      const indicatorY = buttonRect.top - sidebarRect.top;

      this.indicatorPosition = indicatorY; // Aggiorna la posizione della linea
    },

    closeAnalyzeStoryModal() {
      const body = document.querySelector("body");
      this.activeAnalyzeStoryModal = !this.activeAnalyzeStoryModal;
      body.classList.remove("modal-open");
    },
  },
  computed: {
    totalPages() {
      return Math.ceil(this.stories.length / this.storiesPerPage);
    },
    paginatedStories() {
      const start = (this.currentPage - 1) * this.storiesPerPage;
      const end = start + this.storiesPerPage;
      return this.stories.slice(start, end);
    },
  },
  mounted() {
    this.$nextTick(() => {
      this.activeButton = this.$el.querySelector(".btn_chapter"); // Inizializza il primo pulsante come attivo
      this.updateIndicator(); // Imposta la posizione iniziale dell'indicatore
    });
  },
};

// Function needed to show the loaded file name
function handleStoriesUpload(event) {
  const fileInput = event.target;
  const fileNameElement = document.getElementById("file-name");
  const file = fileInput.files[0];

  if (file) {
    fileNameElement.textContent = file.name;
  } else {
    fileNameElement.textContent = "No file selected";
  }
}

// Assicurati che il DOM sia caricato prima di aggiungere l'evento
document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.querySelector(".form-control");
  fileInput.addEventListener("change", handleStoriesUpload);
});
</script>
