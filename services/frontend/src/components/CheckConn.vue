<template>
  <section id="CheckConn">
    <mdb-jumbotron style="margin-bottom: 300px;">
      <h1
        v-if="StatusConn == false"
        class="red-text text-center"
        style="margin-bottom: 100px;"
      >
        Disconnect!!
      </h1>
      <h1
        v-else
        class="light-green-text text-center"
        style="margin-bottom: 100px;"
      >
        Connected!!
      </h1>
      <h1 class="light-green-text text-center" style="margin-bottom: 100px;">
        Login Code: {{ UserCode }}
      </h1>
      <center>
        <mdb-btn color="primary" size="lg" @click="getSetup(), getStatusConn(), count +=1"
          v-if="count == 1">Get Code</mdb-btn
        >
        <a href="https://www.google.com/device" target="_blank"
          ><mdb-btn color="primary" size="lg" v-if="count == 2" @click="count +=1">Google Could</mdb-btn></a
        >
        <mdb-btn color="primary" size="lg" @click="getConnStatus()"
          v-if="count == 3">Check Status</mdb-btn
        >
      </center>
    </mdb-jumbotron>
  </section>
</template>

<script>
import { mdbJumbotron, mdbBtn } from "mdbvue";
import axios from "axios";
export default {
  name: "CheckConn",
  components: {
    mdbJumbotron,
    mdbBtn,
  },
  data() {
    return {
      StatusConn: "",
      UserCode: "",
      LinkLogin: "",
      CheckStatusConn: "",
      count: 1,
    };
  },
  methods: {
    getStatusConn() {
      axios.get("/cloud/status").then((res) => {
        this.StatusConn = res.data.verified;
      });
    },
    getSetup() {
      axios.get("/cloud/setup?verified=false").then((res) => {
        this.UserCode = res.data.user_code;
        this.LinkLogin = res.data.verification_url;
      });
    },
    getConnStatus() {
      axios.get("/cloud/setup?verified=true").then((res) => {
        this.CheckStatusConn = res.data.result;

        if (this.CheckStatusConn == false) {
          alert("Not Login");
          this.StatusConn = false;
        } else if (this.CheckStatusConn == true) {
          alert("Login");
          this.StatusConn = true;
          this.count = 1;
        }
      });
    },
  },

  created() {
    this.getStatusConn();
    //this.getSetup();
    //this.getConnStatus();
  },
};
</script>
