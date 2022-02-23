<template>
  <v-row>
    <v-col cols="1">
      <v-navigation-drawer v-model="drawer" permanent style="display: flex">
        <v-list dense>
          <v-list-item v-for="item in items" :key="item.title" link> 
            <v-list-item-icon style="justify-content: center">
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-icon>
          </v-list-item>
        </v-list>
      </v-navigation-drawer>
    </v-col>
    <v-col cols="11" style="margin-top: 5%">
      <v-row>
        <slot name="tempbox"></slot>
      </v-row>
      <v-row>
        <slot name="helloworld"></slot>
      </v-row>
      <v-row>
        <slot name="chartpage"></slot>
      </v-row>
    </v-col>
  </v-row>
</template>

<script>
export default {
  data() {
    return {
      drawer: true,
      items: [
        { title: "Home", icon: "mdi-home-city" },
        { title: "My Account", icon: "mdi-account" },
        { title: "Users", icon: "mdi-account-group-outline" },
      ],
      mini: true,
    };
  },
};
</script>
