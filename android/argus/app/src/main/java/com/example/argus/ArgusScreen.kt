package com.example.argus

import android.app.Notification
import androidx.annotation.StringRes
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.lifecycle.viewmodel.initializer
import androidx.lifecycle.viewmodel.viewModelFactory
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.example.argus.data.NotificationClient
import com.example.argus.model.NotificationViewModel
import com.example.argus.ui.screens.LoadingScreen
import com.example.argus.ui.screens.LoginScreen
import com.example.argus.ui.screens.NotificationsScreen

enum class ArgusScreen(@StringRes val title: Int) {
    Login(title=R.string.login),
    Notifications(title=R.string.notifications)
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ArgusAppBar(
    currentScreen: ArgusScreen,
    canNavigateBack: Boolean,
    navigateUp: () -> Unit,
    modifier: Modifier = Modifier
) {
    TopAppBar(
        title = { Text(stringResource(currentScreen.title)) },
        colors = TopAppBarDefaults.mediumTopAppBarColors(
            containerColor = MaterialTheme.colorScheme.primaryContainer
        ),
        modifier = modifier,
        navigationIcon = {
            if (canNavigateBack) {
                IconButton(onClick = navigateUp) {
                    Icon(
                        imageVector = Icons.Filled.ArrowBack,
                        contentDescription = stringResource(R.string.back_button)
                    )
                }
            }
        }
    )
}

@Composable
fun ArgusApp(navController: NavHostController = rememberNavController(), notificationClient: NotificationClient) {
    // Get current back stack entry
    val backStackEntry by navController.currentBackStackEntryAsState()

    // Get the name of the current screen
    val currentScreen = ArgusScreen.valueOf(
        backStackEntry?.destination?.route ?: ArgusScreen.Login.name
    )

    var username by remember { mutableStateOf("") }
    var alias by remember { mutableStateOf("") }

    Scaffold(
        topBar = {
            ArgusAppBar(
                currentScreen = currentScreen,
                canNavigateBack = navController.previousBackStackEntry != null,
                navigateUp = { navController.navigateUp() }
            )
        }
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = ArgusScreen.Login.name,
            modifier = Modifier.padding(innerPadding)
        ) {
            composable(route = ArgusScreen.Login.name) {
                LoginScreen { un, a ->
                    username = un
                    alias = a
                    navController.navigate(ArgusScreen.Notifications.name)
                }
            }
            composable(route = ArgusScreen.Notifications.name) {
                val factory: ViewModelProvider.Factory = viewModelFactory {
                    initializer {
                        NotificationViewModel(username, notificationClient)
                    }
                }

                val notificationViewModel: NotificationViewModel = viewModel(factory=factory)

                NotificationsScreen(notificationViewModel)
            }
        }
    }


}

