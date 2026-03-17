from django.shortcuts           import redirect, render, get_object_or_404
from django.urls                import reverse_lazy
from django.contrib             import messages

#MODULOS DE AUTENTICAÇÃO
from django.contrib.auth.models import Group, User
from django.contrib.auth.views  import LoginView as DjangoLoginView, LogoutView
from django.contrib.auth.forms  import AuthenticationForm, UserCreationForm

#mudar senha sem smtp
from django.contrib.auth.views import PasswordChangeView 
from django.contrib.auth.mixins import LoginRequiredMixin

#VIEWS GENERICAS
from django.views.generic       import FormView, CreateView, UpdateView, DeleteView, TemplateView, View, ListView
from django.views.generic.edit          import FormMixin

#FORMS DO PROJETO
from .forms                     import CustomUserCreationForm
from .forms                     import UserGroupForm, GroupForm
from django.db.models           import Q

class LoginView(DjangoLoginView):
    template_name = 'registration/login.html'
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('home:home')

    def form_invalid(self, form):
        """
        Este método é chamado quando o formulário de login é inválido (credenciais incorretas).
        """
        messages.error(self.request, 'Nome de usuário ou senha incorretos. Por favor, tente novamente.')
        return super().form_invalid(form)


class LogoutView(LogoutView):
    next_page = reverse_lazy('login:login') 

#mudar senha com smtp
class CustomPasswordChangeView(PasswordChangeView):
    template_name = "accounts/novasenha/password_change.html"
    success_url = reverse_lazy("accounts:password_change_done")
    
    def form_valid(self, form):
        messages.success(self.request, "Senha alterada com sucesso!")
        return super().form_valid(form)

#grupos
class UserGroupHome(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/accountstools.html'


class UserGroupLinkView(LoginRequiredMixin, FormView):
    template_name = 'accounts/user_group_link.html'
    form_class = UserGroupForm
    success_url = reverse_lazy('accounts:userGroupLink')

    def form_valid(self, form):
        user = form.cleaned_data['user']
        group = form.cleaned_data['group']

        if group in user.groups.all():
            messages.warning(self.request, f"O usuário '{user.username}' já pertence ao grupo '{group.name}'.")
        else:
            user.groups.add(group)
            messages.success(self.request, f"Grupo '{group.name}' vinculado ao usuário '{user.username}' com sucesso.")

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lista todos os usuários com seus grupos
        context['users_with_groups'] = User.objects.prefetch_related('groups').all()
        return context
    

class UserGroupUnlinkView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        group_id = request.POST.get('group_id')

        user = get_object_or_404(User, pk=user_id)
        group = get_object_or_404(Group, pk=group_id)

        if group in user.groups.all():
            user.groups.remove(group)
            messages.success(request, f"Usuário '{user.username}' removido do grupo '{group.name}' com sucesso.")
        else:
            messages.warning(request, f"O usuário '{user.username}' não pertence ao grupo '{group.name}'.")

        # Redireciona de volta para a página de vínculo/desvínculo
        return redirect(reverse_lazy('accounts:userGroupLink'))


class GroupRegisterView(LoginRequiredMixin, FormMixin, ListView):
    model = Group
    form_class = GroupForm
    template_name = 'accounts/group/group_form.html'   
    context_object_name = 'group_list' 
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset().order_by('name')
        query = self.request.GET.get('q') 

        if query:
            # Filtra por username ou email (ou outros campos que desejar)
            queryset = queryset.filter(Q(name__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form() # Adiciona uma instância do formulário ao contexto
        return context

    def post(self, request, *args, **kwargs):
        # O object_list é necessário para o FormMixin funcionar corretamente
        self.object_list = self.get_queryset()
        form = self.get_form()

        if form.is_valid():
            # A lógica de save do formulário já cuida da criptografia da senha
            form.save()
            messages.success(self.request, "Grupo cadastrado com sucesso!")
            return self.form_valid(form)
        else:
            messages.error(self.request, "Erro ao cadastrar Grupo. Verifique os dados.")
            return self.form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        # Garante que o formulário com erros seja passado de volta ao contexto
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        # Redireciona para a mesma página após o sucesso, para exibir a lista atualizada
        return reverse_lazy('accounts:register') # Certifique-se de que 'user_list_create' é o nome da URL para esta view




class GroupDeleteView(LoginRequiredMixin, DeleteView):
    model = Group
    template_name = 'accounts/group/group_delete.html'
    success_url = reverse_lazy('accounts:registerGroup')
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        confirm_name = request.POST.get("confirm_name", "").strip().lower()
        group = self.object.name.strip().lower()

        if confirm_name == group:
            messages.success(request, f"Grupo '{self.object.name}' excluído com sucesso.")
            return super().post(request, *args, **kwargs)
        else:
            return render(request, self.template_name, {
                'object': self.object,
                'error_message': "Grupo digitado não confere com o grupo cadastrado."
            })

    def get_success_url(self):        
        return reverse_lazy('accounts:registerGroup')

#usuarios
class UserRegisterView(LoginRequiredMixin, FormView, ListView):
    model = User
    form_class = UserCreationForm
    template_name = 'accounts/users/user_form.html'   
    context_object_name = 'users_list' # Nome da variável no template para a lista de usuários
    paginate_by = 15 # Opcional: para paginar a lista de usuários

    def get_queryset(self):
        queryset = super().get_queryset().order_by('username')
        query = self.request.GET.get('q') # Pega o parâmetro de pesquisa 'q' da URL

        if query:
            # Filtra por username ou email (ou outros campos que desejar)
            queryset = queryset.filter(Q(username__icontains=query) | Q(email__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form() # Adiciona uma instância do formulário ao contexto
        return context

    def post(self, request, *args, **kwargs):
        # O object_list é necessário para o FormMixin funcionar corretamente
        self.object_list = self.get_queryset()
        form = self.get_form()

        if form.is_valid():
            # A lógica de save do formulário já cuida da criptografia da senha
            form.save()
            messages.success(self.request, "Usuário cadastrado com sucesso!")
            return self.form_valid(form)
        else:
            messages.error(self.request, "Erro ao cadastrar usuário. Verifique os dados.")
            return self.form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        # Garante que o formulário com erros seja passado de volta ao contexto
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        # Redireciona para a mesma página após o sucesso, para exibir a lista atualizada
        return reverse_lazy('accounts:register') # Certifique-se de que 'user_list_create' é o nome da URL para esta view


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'accounts/users/user_delete.html'
    success_url = reverse_lazy('accounts:register')
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        confirm_name = request.POST.get("confirm_name", "").strip().lower()
        username = self.object.username.strip().lower()

        if confirm_name == username:
            messages.success(request, f"Usuário '{self.object.username}' excluído com sucesso.")
            return super().post(request, *args, **kwargs)
        else:
            return render(request, self.template_name, {
                'object': self.object,
                'error_message': "O login digitado não confere com o login cadastrado."
            })

    def get_success_url(self):        
        return reverse_lazy('accounts:register')
   



    
