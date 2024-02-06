package com.example.argus.model

import android.content.Context
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.launch

val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "user")


private object StorageKey {
    val username = stringPreferencesKey("username")
    val alias = stringPreferencesKey("alias")
    val loggedIn = booleanPreferencesKey("loggedIn")
}


sealed interface UserState {
    data class LoggedIn(val username: String, val alias: String) : UserState
    data object LoggedOut : UserState
}

class UserViewModel(private val context: Context) : ViewModel() {
    var userState: UserState by mutableStateOf(UserState.LoggedOut)

    init {
        restore()
    }

    fun logIn(username: String, alias: String) {
        store(username, alias)
        userState = UserState.LoggedIn(username, alias)
    }

    fun logOut() {
        clean()
        userState = UserState.LoggedOut
    }

    private fun restore() {
        viewModelScope.launch{
            context.dataStore.data.collect { preferences ->
                val loggedIn = preferences[StorageKey.loggedIn] ?: false

                if (loggedIn) {
                    userState = UserState.LoggedIn(
                        username = preferences[StorageKey.username]!!,
                        alias = preferences[StorageKey.alias]!!
                    )
                }
            }
        }
    }

    private fun store(username: String, alias: String) {
        viewModelScope.launch{
            context.dataStore.edit { preferences ->
                preferences[StorageKey.loggedIn] = true
                preferences[StorageKey.username] = username
                preferences[StorageKey.alias] = alias
            }
        }
    }

    private fun clean() {
        viewModelScope.launch{
            context.dataStore.edit { preferences ->
                preferences[StorageKey.loggedIn] = false
                preferences.remove(StorageKey.username)
                preferences.remove(StorageKey.alias)
            }
        }
    }
}