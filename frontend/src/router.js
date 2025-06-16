import { createRouter, createWebHistory } from "vue-router";
import HomeView from "./views/HomeView.vue";
import DatabaseConnections from "./views/DatabaseConnections.vue";
import TableView from "@/views/TableView.vue"
import SemanticImport from "@/views/SemanticImport.vue";
import ImportarPbit from "./views/ImportarPbit.vue";

const routes = [
  { path: "/", component: HomeView },
  { path: "/connections", component: DatabaseConnections },
  { path: "/tables", component: TableView},
  { path: "/semantic-import", component: SemanticImport },
  { path: "/importar-pbit", component: ImportarPbit }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
