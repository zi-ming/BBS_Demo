BBS_Demo
===================

##### 该项目模仿了“虎嗅”的网页效果，实现了新闻资讯的分类、浏览、对新闻详细内容的查看，评论；借助Django自带的后台实现对新闻和评论以及用户的管理；除此之外，还实现了用户在线聊天的功能。

#### 知识要点：
>>Django<br>
>>HTML/CSS/JS<br>
>>BootStrap<br>
>>JQuery<br>

* Author： 李梓铭<br>
* E-mail：1564603397@qq.com

### 实现思路
#### 一. 确定需求
>1.实现新闻分类<br>
2.实现用户注册和登陆以及注销<br>
3.能够实现新闻详细内容的浏览（无论用户是否登陆，均可浏览新闻内容）<br>
4.用户可以查看新闻评论和点赞数量，已登录的用户可以发表评论以及点赞<br>
5.已登录用户可以发帖和实现在线聊天（包括一对一聊天以及群聊）<br>
6.如果用户想评论、点赞或发帖，但没有登陆，提示用户先登陆，再操作<br>

#### 二. 确定界面布局
>1.首页显示新闻分类、新闻列表、以及用户登陆、发帖等信息<br>
>>(1) 布局分为两层布局，第一层显示新闻分类信息（左侧）、用户登陆信息、发帖（右侧）等功能界面，是该网站的菜单栏；第二层显示新闻列表信息<br>
(2) 如果用户未登陆，则菜单栏的右侧只显示“登陆”、“发帖”等功能界面<br>
(3) 要求新闻列表每一项的显示信息包括如下：新闻图片、新闻标题、作者、发表时间、简介、评论数以及点赞数<br>
  
>2.点击新闻列表的某一条新闻时，浏览器在新的标签显示对应新闻的详细信息（标题、发表时间、作者、内容）
>>(1) 新闻详细信息页面分为六层：<br>
>>>a) 第一层：显示新闻标题<br>
b) 第二层：显示发表时间、作者<br>
c) 第三层：显示新闻内容<br>
d) 第四层：显示评论输入框（如果用户已登录，若未登录，则显示登陆按钮）<br>
e) 第五层：显示评论数量以及点赞数量（登陆与否均可看到）<br>
f) 第六层：树型显示评论内容<br>

3.发帖界面包括基本信息（新闻标题、分类、简介、内容、图片上传以及新闻的状态）的填写<br>

4.聊天界面设计成左右两边的布局：左边显示联系人（好友以及群组）；右面分为上下两部分：上面显示聊天信息，下面显示文本输入框以及发送按钮<br>

#### 三. 建立数据库模型（models）
>1. BBS.models
>>* 因为该项目的对象主要有：文章（Article）、评论（Comment）、新闻分类（Category）、用户（UserProfile），所以在BBS.models中创建了以下4个Model对象：
```
class Article(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey("Category")
    brief = models.CharField(max_length=255,blank=True,null=True)
    content = models.TextField()
    author = models.ForeignKey("UserProfile")
    pub_date = models.DateTimeField(auto_now_add=True)
    last_modify = models.DateTimeField(auto_now=True)
    priority = models.SmallIntegerField(default=1000)
    head_img = models.ImageField(upload_to="uploads")
    status_choice = (('draft',u'草稿'),
                     ('published', u'已发布'),
                     ('hidden', u'隐藏'),
                     )
    status = models.CharField(max_length=32,choices=status_choice, default="draft")

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey("Article")
    parent_comment = models.ForeignKey("self",related_name="child_comments",
                                       blank=True,null=True)
    comment_choice = ((0,u"评论"),
                      (1, u"点赞"),
                      )
    comment_type = models.SmallIntegerField(choices=comment_choice, default=0)
    user = models.ForeignKey("UserProfile")
    comment = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.comment_type == 0 and len(self.comment.strip())==0:
            raise ValidationError(u"评论不能为空")

    def __str__(self):
        return "%s, P:%s, %s, %s"%(self.article,
                                   self.parent_comment.id if self.parent_comment is not None
                                   else "Null", self.user, self.comment)

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    brief = models.CharField(max_length=255,blank=True,null=True)
    set_as_top_menu = models.BooleanField(default=False)
    position = models.SmallIntegerField()
    admin = models.ForeignKey("UserProfile")
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=32)
    signature = models.TextField(null=True,blank=True)
    head_img = models.ImageField(upload_to="uploads",null=True,blank=True)

    # for webchat
    friends = models.ManyToManyField("self", related_name="friends_userprofile", blank=True)


    def __str__(self):
        return self.name
```
>>* 只要你在Model类中对属性设置好ForeignKey，那么Django会自动管理两张表的关系，省去了构造中间表的麻烦，非常方便。

>>2. 前端布局实现
>>>(1) 创建一个模板Base.html，该模板是从[BootStrap](http://v3.bootcss.com/examples/navbar-fixed-top/)里刮下来的，精简了一下，无论是新闻主页、新闻详细内容页面、发帖页面以及在线聊天页面都需要继承自该模板，这样有助于减少代码冗余，方便维护。
>>>(2) 网站主页因为是继承自模板，所以所以实现的代码量不多，只需把新闻列表项设计好就行。
>>>(3) 新闻内容详细信息页也是通过BootStrap中的Example改造而成。
>>>(4) 发帖页面的实现也不难，因为Django中的ModelForm可以自动实现页面的布局，至于内容输入框，可以调用ckeditor的模板实现。
>>>(5) 在线聊天页面的实现比较粗糙，主要是那时快要考试，所以只实现了功能，没有对界面做进一步的优化。
>>>(6) 填充静态数据测试是否与预期效果一致。

>>3. 
