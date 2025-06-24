import { useEffect, useState } from "react";

import { Clock, Edit3, Loader2, Plus, Send, Settings, Trash2 } from "lucide-react";

interface Channel {
  id: number;
  name: string;
  channel_id: string;
  bot_token: string;
  language: string;
  created_at?: string;
}

interface ChannelGroup {
  id: number;
  name: string;
  channels: Channel[];
}

interface PostContent {
  channel_id: number;
  content: string;
}

interface Post {
  id: number;
  group_id: number;
  publish_time: string;
  status: string;
  created_at: string;
  contents: PostContent[]; // массив: { channel_id, content }
}

const API_BASE_URL = "http://localhost:8015";

export default function TelegramContentManager() {
  // State
  const [activeTab, setActiveTab] = useState<"content" | "settings">("content");
  const [channelGroups, setChannelGroups] = useState<ChannelGroup[]>([]);
  const [selectedGroup, setSelectedGroup] = useState<number | null>(null);
  const [newGroupName, setNewGroupName] = useState("");
  const [newChannelForm, setNewChannelForm] = useState({
    name: "",
    channel_id: "",
    bot_token: "",
    language: "",
  });
  const [posts, setPosts] = useState<Post[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [editingGroup, setEditingGroup] = useState<number | null>(null);
  const [contentForm, setContentForm] = useState<{
    publishTime: string;
    publishNow: boolean;
    channelContents: Record<number, string>;
  }>({
    publishTime: "",
    publishNow: false,
    channelContents: {},
  });

  // --- API FUNCTIONS ---

  // Groups
  const fetchChannelGroups = async () => {
    const response = await fetch(`${API_BASE_URL}/channel-groups/`);
    if (!response.ok) throw new Error("Failed to fetch channel groups");
    return await response.json();
  };

  const createChannelGroup = async (name: string) => {
    const response = await fetch(`${API_BASE_URL}/channel-groups/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    });
    if (!response.ok) throw new Error("Failed to create group");
    return await response.json();
  };

  const deleteChannelGroup = async (groupId: number) => {
    const response = await fetch(`${API_BASE_URL}/channel-groups/${groupId}`, {
      method: "DELETE",
    });
    if (!response.ok) throw new Error("Failed to delete group");
  };

  // Channels
  const addChannel = async (groupId: number, data: typeof newChannelForm) => {
    const response = await fetch(`${API_BASE_URL}/channel-groups/${groupId}/channels/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error("Failed to add channel");
    return await response.json();
  };

  const deleteChannel = async (channelId: number) => {
    const response = await fetch(`${API_BASE_URL}/channels/${channelId}`, {
      method: "DELETE",
    });
    if (!response.ok) throw new Error("Failed to delete channel");
  };

  // Posts
  const fetchPosts = async () => {
    const response = await fetch(`${API_BASE_URL}/posts/`);
    if (!response.ok) throw new Error("Failed to fetch posts");
    return await response.json();
  };

  const createPost = async (data: {
    group_id: number;
    publish_time: string;
    publish_now: boolean;
    contents: PostContent[];
  }) => {
    const response = await fetch(`${API_BASE_URL}/posts/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error("Failed to create post");
    return await response.json();
  };

  const deletePost = async (postId: number) => {
    const response = await fetch(`${API_BASE_URL}/posts/${postId}`, {
      method: "DELETE",
    });
    if (!response.ok) throw new Error("Failed to delete post");
  };

  // --- EFFECTS ---

  useEffect(() => {
    setIsLoading(true);
    Promise.all([fetchChannelGroups(), fetchPosts()])
      .then(([groups, posts]) => {
        setChannelGroups(groups);
        setPosts(posts);
        if (groups.length > 0) {
          setSelectedGroup(groups[0].id);
        }
      })
      .catch(() => alert("Ошибка загрузки данных"))
      .finally(() => setIsLoading(false));
  }, []);

  useEffect(() => {
    if (selectedGroup !== null) {
      const group = channelGroups.find((g) => g.id === selectedGroup);
      const channelContents: Record<number, string> = {};
      group?.channels.forEach((ch) => {
        channelContents[ch.id] = "";
      });
      setContentForm((prev) => ({
        ...prev,
        channelContents,
      }));
    }
  }, [selectedGroup, channelGroups]);

  // --- HANDLERS ---

  const handleAddGroup = async () => {
    if (!newGroupName.trim()) return;
    setIsLoading(true);
    try {
      const group = await createChannelGroup(newGroupName.trim());
      setChannelGroups((prev) => [...prev, group]);
      setNewGroupName("");
    } catch {
      alert("Не удалось создать группу");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteGroup = async (groupId: number) => {
    if (!window.confirm("Удалить группу и все её каналы?")) return;
    setIsLoading(true);
    try {
      await deleteChannelGroup(groupId);
      setChannelGroups((prev) => prev.filter((g) => g.id !== groupId));
      if (selectedGroup === groupId) setSelectedGroup(null);
    } catch {
      alert("Ошибка при удалении группы");
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddChannel = async (groupId: number) => {
    if (!newChannelForm.name || !newChannelForm.channel_id || !newChannelForm.bot_token)
      return alert("Заполни все обязательные поля (название, id канала, токен)");
    setIsLoading(true);
    try {
      const ch = await addChannel(groupId, newChannelForm);
      setChannelGroups((prev) =>
        prev.map((g) =>
          g.id === groupId ? { ...g, channels: [...g.channels, ch] } : g
        )
      );
      setNewChannelForm({
        name: "",
        channel_id: "",
        bot_token: "",
        language: "",
      });
      setEditingGroup(null);
    } catch {
      alert("Ошибка при добавлении канала");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteChannel = async (groupId: number, channelId: number) => {
    if (!window.confirm("Удалить канал?")) return;
    setIsLoading(true);
    try {
      await deleteChannel(channelId);
      setChannelGroups((prev) =>
        prev.map((g) =>
          g.id === groupId
            ? { ...g, channels: g.channels.filter((c) => c.id !== channelId) }
            : g
        )
      );
    } catch {
      alert("Ошибка при удалении канала");
    } finally {
      setIsLoading(false);
    }
  };

  const handlePublishContent = async () => {
    if (!selectedGroup) return alert("Выбери группу");
    const group = channelGroups.find((g) => g.id === selectedGroup);
    if (!group) return;

    const contents: PostContent[] = group.channels
      .map((ch) => ({
        channel_id: ch.id,
        content: contentForm.channelContents[ch.id] || "",
      }))
      .filter((c) => c.content.trim() !== "");

    if (!contents.length) return alert("Введи текст хотя бы для одного канала");

    try {
      setIsLoading(true);
      const post = await createPost({
        group_id: selectedGroup,
        publish_time: contentForm.publishNow
          ? new Date().toISOString()
          : contentForm.publishTime,
        publish_now: contentForm.publishNow,
        contents,
      });
      setPosts((prev) => [post, ...prev]);
      // reset form
      const channelContents: Record<number, string> = {};
      group.channels.forEach((ch) => {
        channelContents[ch.id] = "";
      });
      setContentForm({
        publishNow: false,
        publishTime: "",
        channelContents,
      });
      alert("Пост создан!");
    } catch {
      alert("Ошибка при создании поста");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeletePost = async (postId: number) => {
    if (!window.confirm("Удалить пост?")) return;
    setIsLoading(true);
    try {
      await deletePost(postId);
      setPosts((prev) => prev.filter((p) => p.id !== postId));
    } catch {
      alert("Ошибка при удалении поста");
    } finally {
      setIsLoading(false);
    }
  };

  // --- RENDER ---

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
        <Loader2 className="animate-spin h-12 w-12 text-blue-500 mx-auto mb-4" />
        <div className="text-gray-600 text-lg font-medium">Загрузка...</div>
      </div>
    );
  }

  const selectedGroupData = channelGroups.find((g) => g.id === selectedGroup);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm shadow-xl border-b border-gray-200/50 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-6 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Send className="w-8 h-8 text-blue-600" />
            <h1 className="text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">
              Telegram Content Manager
            </h1>
          </div>
          <nav className="flex gap-3">
            <button
              onClick={() => setActiveTab("content")}
              className={`px-8 py-4 rounded-2xl font-semibold transition-all duration-300 flex items-center gap-3 transform hover:scale-105 ${activeTab === "content"
                ? "bg-gradient-to-r from-blue-500 to-indigo-600 text-white shadow-xl shadow-blue-500/30"
                : "bg-white/70 text-gray-700 hover:bg-white hover:shadow-lg border border-gray-200/50"
                }`}
            >
              <Send className="w-5 h-5" />
              Контент
            </button>
            <button
              onClick={() => setActiveTab("settings")}
              className={`px-8 py-4 rounded-2xl font-semibold transition-all duration-300 flex items-center gap-3 transform hover:scale-105 ${activeTab === "settings"
                ? "bg-gradient-to-r from-blue-500 to-indigo-600 text-white shadow-xl shadow-blue-500/30"
                : "bg-white/70 text-gray-700 hover:bg-white hover:shadow-lg border border-gray-200/50"
                }`}
            >
              <Settings className="w-5 h-5" />
              Настройки
            </button>
          </nav>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-10">
        {/* SETTINGS */}
        {activeTab === "settings" && (
          <div className="space-y-10">
            {/* Создать группу */}
            <section className="bg-white/80 rounded-3xl shadow-xl border border-gray-200/50 p-8">
              <div className="flex items-center gap-4 mb-6">
                <Plus className="w-7 h-7 text-green-600" />
                <h2 className="text-2xl font-bold">Создать группу каналов</h2>
              </div>
              <div className="flex gap-4 items-end">
                <input
                  type="text"
                  value={newGroupName}
                  onChange={(e) => setNewGroupName(e.target.value)}
                  placeholder="Название группы"
                  className="border-2 border-gray-200 rounded-xl px-6 py-4 text-lg font-medium w-80"
                />
                <button
                  onClick={handleAddGroup}
                  className="bg-gradient-to-r from-green-500 to-emerald-600 text-white px-8 py-4 rounded-2xl font-bold transition-all"
                >
                  <Plus className="w-6 h-6" /> Добавить
                </button>
              </div>
            </section>
            {/* Список групп */}
            {channelGroups.map((group) => (
              <section key={group.id} className="bg-white/80 rounded-3xl shadow-xl border border-gray-200/50 p-8 mb-8">
                <div className="flex justify-between items-center mb-4">
                  <div>
                    <h3 className="text-xl font-bold">{group.name}</h3>
                    <p className="text-gray-500">{group.channels.length} канал(ов)</p>
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => setEditingGroup(editingGroup === group.id ? null : group.id)}
                      className="p-2 rounded-2xl text-gray-500 hover:text-blue-600 hover:bg-blue-50 transition-all"
                    >
                      <Edit3 className="w-6 h-6" />
                    </button>
                    <button
                      onClick={() => handleDeleteGroup(group.id)}
                      className="p-2 rounded-2xl text-red-500 hover:text-red-700 hover:bg-red-50 transition-all"
                    >
                      <Trash2 className="w-6 h-6" />
                    </button>
                  </div>
                </div>
                {/* Добавление каналов */}
                {editingGroup === group.id && (
                  <div className="mb-4">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
                      <input
                        type="text"
                        placeholder="Название"
                        value={newChannelForm.name}
                        onChange={(e) =>
                          setNewChannelForm((prev) => ({ ...prev, name: e.target.value }))
                        }
                        className="border-2 border-gray-200 rounded-xl px-4 py-3"
                      />
                      <input
                        type="text"
                        placeholder="@channel_id"
                        value={newChannelForm.channel_id}
                        onChange={(e) =>
                          setNewChannelForm((prev) => ({
                            ...prev,
                            channel_id: e.target.value,
                          }))
                        }
                        className="border-2 border-gray-200 rounded-xl px-4 py-3"
                      />
                      <input
                        type="password"
                        placeholder="Bot Token"
                        value={newChannelForm.bot_token}
                        onChange={(e) =>
                          setNewChannelForm((prev) => ({
                            ...prev,
                            bot_token: e.target.value,
                          }))
                        }
                        className="border-2 border-gray-200 rounded-xl px-4 py-3"
                      />
                      <input
                        type="text"
                        placeholder="Язык (опц.)"
                        value={newChannelForm.language}
                        onChange={(e) =>
                          setNewChannelForm((prev) => ({
                            ...prev,
                            language: e.target.value,
                          }))
                        }
                        className="border-2 border-gray-200 rounded-xl px-4 py-3"
                      />
                    </div>
                    <button
                      onClick={() => handleAddChannel(group.id)}
                      className="bg-gradient-to-r from-blue-500 to-indigo-600 text-white px-6 py-3 rounded-xl font-bold"
                    >
                      <Plus className="w-5 h-5" /> Добавить канал
                    </button>
                  </div>
                )}
                {/* Список каналов */}
                {group.channels.length > 0 && (
                  <div className="space-y-3">
                    <h4 className="text-lg font-bold mb-2">Каналы:</h4>
                    {group.channels.map((ch) => (
                      <div key={ch.id} className="flex items-center justify-between bg-gradient-to-r from-gray-50 to-blue-50 p-4 rounded-xl border-2 border-gray-200">
                        <div>
                          <span className="font-bold text-gray-900">{ch.name}</span>
                          <span className="ml-3 text-gray-500">{ch.channel_id}</span>
                          {ch.language && (
                            <span className="ml-3 px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs">
                              {ch.language}
                            </span>
                          )}
                        </div>
                        <button
                          onClick={() => handleDeleteChannel(group.id, ch.id)}
                          className="p-2 text-red-500 hover:text-red-700 hover:bg-red-50 rounded-xl"
                        >
                          <Trash2 className="w-5 h-5" />
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </section>
            ))}
          </div>
        )}

        {/* CONTENT */}
        {activeTab === "content" && (
          <div className="grid grid-cols-1 xl:grid-cols-2 gap-10">
            {/* Создать пост */}
            <section className="bg-white/80 rounded-3xl shadow-xl border border-gray-200/50 p-8">
              <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
                <Send className="w-7 h-7 text-blue-600" />
                Новый пост
              </h2>
              <div className="mb-4">
                <label className="block font-bold mb-2">Группа:</label>
                <select
                  value={selectedGroup ?? ""}
                  onChange={(e) => setSelectedGroup(Number(e.target.value))}
                  className="border-2 border-gray-200 rounded-xl px-4 py-3 w-full"
                >
                  <option value="">Выбери группу</option>
                  {channelGroups.map((g) => (
                    <option key={g.id} value={g.id}>
                      {g.name}
                    </option>
                  ))}
                </select>
              </div>
              {selectedGroupData && (
                <div className="space-y-5">
                  <div>
                    <label className="font-bold block mb-2">Текст для каждого канала:</label>
                    {selectedGroupData.channels.length === 0 ? (
                      <div className="text-gray-400 italic">В этой группе пока нет каналов.</div>
                    ) : (
                      <div className="space-y-4">
                        {selectedGroupData.channels.map((ch) => (
                          <div key={ch.id}>
                            <span className="font-bold text-gray-700">{ch.name}</span>
                            <textarea
                              value={contentForm.channelContents[ch.id] || ""}
                              onChange={(e) =>
                                setContentForm((prev) => ({
                                  ...prev,
                                  channelContents: {
                                    ...prev.channelContents,
                                    [ch.id]: e.target.value,
                                  },
                                }))
                              }
                              className="mt-2 w-full border-2 border-gray-200 rounded-xl px-4 py-3 text-lg"
                              rows={3}
                              placeholder={`Текст для "${ch.name}"`}
                            />
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                  <div className="flex items-center gap-4">
                    <input
                      type="checkbox"
                      checked={contentForm.publishNow}
                      onChange={(e) =>
                        setContentForm((prev) => ({
                          ...prev,
                          publishNow: e.target.checked,
                        }))
                      }
                    />
                    <span>Опубликовать сейчас</span>
                  </div>
                  {!contentForm.publishNow && (
                    <div>
                      <label className="block font-bold mb-2">Дата и время публикации:</label>
                      <input
                        type="datetime-local"
                        value={contentForm.publishTime}
                        onChange={(e) =>
                          setContentForm((prev) => ({
                            ...prev,
                            publishTime: e.target.value,
                          }))
                        }
                        className="border-2 border-gray-200 rounded-xl px-4 py-3 w-72"
                      />
                    </div>
                  )}
                  <button
                    onClick={handlePublishContent}
                    className="bg-gradient-to-r from-blue-500 to-indigo-600 text-white px-8 py-4 rounded-2xl font-bold flex items-center gap-3"
                  >
                    <Send className="w-5 h-5" />
                    Опубликовать
                  </button>
                </div>
              )}
            </section>
            {/* Список постов */}
            <section className="bg-white/80 rounded-3xl shadow-xl border border-gray-200/50 p-8">
              <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
                <Clock className="w-7 h-7 text-indigo-600" />
                История постов
              </h2>
              {posts.length === 0 ? (
                <div className="text-gray-400 italic">Нет постов</div>
              ) : (
                <div className="space-y-5">
                  {posts.map((p) => (
                    <div
                      key={p.id}
                      className="p-4 rounded-xl border border-gray-200 bg-gradient-to-br from-gray-50 to-indigo-50 flex flex-col gap-2 shadow"
                    >
                      <div className="flex justify-between items-center">
                        <div>
                          <span className="font-bold text-gray-900">Группа: </span>
                          <span className="text-gray-700">{p.group_id}</span>
                        </div>
                        <span
                          className={`inline-block px-4 py-1 rounded-full font-bold text-sm ${p.status === "published"
                            ? "bg-green-200 text-green-800"
                            : p.status === "scheduled"
                              ? "bg-yellow-200 text-yellow-800"
                              : "bg-red-200 text-red-800"
                            }`}
                        >
                          {p.status}
                        </span>
                      </div>
                      <div>
                        <span className="font-bold text-gray-900">Дата публикации: </span>
                        <span className="text-gray-700">
                          {new Date(p.publish_time).toLocaleString()}
                        </span>
                      </div>
                      <div>
                        <span className="font-bold">Тексты по каналам:</span>
                        <ul className="pl-4 list-disc">
                          {p.contents.map((c, i) => {
                            const channelName =
                              channelGroups
                                .find((g) => g.id === p.group_id)
                                ?.channels.find((ch) => ch.id === c.channel_id)?.name || c.channel_id;
                            return (
                              <li key={i}>
                                <span className="font-bold">{channelName}: </span>
                                <span>{c.content}</span>
                              </li>
                            );
                          })}
                        </ul>
                      </div>
                      <button
                        onClick={() => handleDeletePost(p.id)}
                        className="ml-auto px-4 py-2 bg-red-100 text-red-600 rounded-xl hover:bg-red-200 font-bold mt-2"
                      >
                        <Trash2 className="w-4 h-4 inline" /> Удалить
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </section>
          </div>
        )}
      </main>
    </div>
  );
}
