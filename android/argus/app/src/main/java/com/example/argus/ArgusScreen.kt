package com.example.argus

import androidx.annotation.StringRes
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.platform.LocalContext
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.lifecycle.viewmodel.initializer
import androidx.lifecycle.viewmodel.viewModelFactory
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.example.argus.data.AuthenticationClient
import com.example.argus.data.NotificationClient
import com.example.argus.model.NotificationViewModel
import com.example.argus.model.UserState
import com.example.argus.model.UserViewModel
import com.example.argus.notifications.Manager
import com.example.argus.ui.screens.LoginScreen
import com.example.argus.ui.screens.NotificationScreen
import com.example.argus.ui.screens.NotificationsScreen

enum class ArgusScreen(@StringRes val title: Int) {
    Login(title=R.string.login),
    Notifications(title=R.string.notifications),
    Notification(title= R.string.notification_details)
}

@Composable
fun Redirect(navController: NavHostController, currentScreen : ArgusScreen, destinationScreen : ArgusScreen) {
    val backStackEntry by navController.currentBackStackEntryAsState()
    val destination = backStackEntry?.destination?.route ?: currentScreen.name

    if (destination == currentScreen.name) {
        navController.navigate(destinationScreen.name)
    }
}

@Composable
fun ArgusApp(navController: NavHostController = rememberNavController(),
             authenticationClient: AuthenticationClient,
             notificationClient: NotificationClient,
             notificationManager: Manager) {
    val context = LocalContext.current

    val userFactory: ViewModelProvider.Factory = viewModelFactory {
        initializer {
            UserViewModel(context)
        }
    }

    val userViewModel : UserViewModel = viewModel(factory = userFactory)
    val userState = userViewModel.userState

    NavHost(
        navController = navController,
        startDestination = ArgusScreen.Login.name,
    ) {
        composable(route = ArgusScreen.Login.name) {
            when (userState) {
                is UserState.LoggedIn -> {
                    Redirect(
                        navController = navController,
                        currentScreen = ArgusScreen.Login,
                        destinationScreen = ArgusScreen.Notifications
                    )
                }
                is UserState.LoggedOut -> LoginScreen(authenticationClient) { username, alias ->
                    userViewModel.logIn(username, alias)
                }
            }

        }
        composable(route = ArgusScreen.Notifications.name) {
            when (userState) {
                is UserState.LoggedIn -> {
                    val factory: ViewModelProvider.Factory = viewModelFactory {
                        initializer {
                            NotificationViewModel(userState.username, notificationClient, notificationManager)
                        }
                    }

                    NotificationsScreen(factory, navigateUp = {
                        userViewModel.logOut()
                    }, onNotificationClick =  { notification ->
                        userViewModel.notification = notification
                        navController.navigate(ArgusScreen.Notification.name)
                    })
                }
                is UserState.LoggedOut -> {
                    Redirect(
                        navController = navController,
                        currentScreen = ArgusScreen.Notifications,
                        destinationScreen = ArgusScreen.Login
                    )
                }
            }
        }
        composable(route = ArgusScreen.Notification.name) {
            if (!userViewModel.notification.read)
                notificationClient.markRead(userViewModel.notification)

            userViewModel.notification.read = true

            NotificationScreen(userViewModel.notification, notificationClient, navigateUp = {
                navController.navigateUp()
            })
        }
    }
}

