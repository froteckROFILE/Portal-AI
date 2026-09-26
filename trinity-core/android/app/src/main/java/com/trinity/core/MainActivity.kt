package com.trinity.core
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.foundation.text.selection.SelectionContainer
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.launch
class MainActivity : ComponentActivity() { override fun onCreate(savedInstanceState: Bundle?) { super.onCreate(savedInstanceState); setContent { MaterialTheme { TrinityScreen() } } } }
@Composable fun TrinityScreen() {
 var prompt by remember { mutableStateOf("") }; var mode by remember { mutableStateOf("arena") }; var result by remember { mutableStateOf("") }; var status by remember { mutableStateOf("Ready") }; var candidates by remember { mutableStateOf<List<Candidate>>(emptyList()) }; val scope=rememberCoroutineScope()
 Scaffold(topBar={TopAppBar(title={Text("TRINITY CORE")})}) { pad -> Column(Modifier.padding(pad).padding(16.dp).verticalScroll(rememberScrollState())) {
 Text("Parallel Multi-AI Decision Engine",style=MaterialTheme.typography.titleMedium); Spacer(Modifier.height(14.dp))
 OutlinedTextField(value=prompt,onValueChange={prompt=it},label={Text("What do you want to solve?")},modifier=Modifier.fillMaxWidth().height(180.dp)); Spacer(Modifier.height(10.dp))
 Row { FilterChip(selected=mode=="parallel",onClick={mode="parallel"},label={Text("PARALLEL")}); Spacer(Modifier.width(8.dp)); FilterChip(selected=mode=="arena",onClick={mode="arena"},label={Text("ARENA")}) }
 Spacer(Modifier.height(12.dp)); Button(enabled=prompt.isNotBlank()&&status!="Running",onClick={scope.launch { status="Running"; result=""; candidates=emptyList(); try { val r=Api.service.solve(SolveRequest(prompt,mode)); candidates=r.candidates; result=r.final; status="Complete" } catch(e:Exception){status="Error";result=e.message?:"Request failed"} }},modifier=Modifier.fillMaxWidth()){Text("RUN COUNCIL")}
 Spacer(Modifier.height(12.dp)); Text("Status: $status")
 if(candidates.isNotEmpty()){Spacer(Modifier.height(12.dp));Text("Independent first pass",style=MaterialTheme.typography.titleMedium);candidates.forEach{c->Card(Modifier.fillMaxWidth().padding(vertical=4.dp)){Column(Modifier.padding(10.dp)){Text("${c.provider}: ${if(c.ok) "completed" else "failed"}");if(!c.ok)Text(c.error?:"Unknown provider error")}}}}
 if(result.isNotBlank()){Spacer(Modifier.height(16.dp));Text("FINAL PRODUCT",style=MaterialTheme.typography.titleLarge);Spacer(Modifier.height(6.dp));SelectionContainer{Text(result)}} } }
}
