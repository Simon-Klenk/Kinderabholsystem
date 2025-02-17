import { mount, flushPromises } from '@vue/test-utils'
import MessagesContainer from '@/views/StateView.vue'
global.fetch = jest.fn()

jest.mock('cross-fetch')
jest.mock('@/components/MessageItem.vue', () => ({
  template: '<div class="message-item-mock"></div>'
}))

describe('MessagesContainer.vue', () => {
  let wrapper
  const mockMessages = [
    { id: 1, content: 'Test 1', created_at: '2025-02-17T10:00:00', status: 'sent' },
    { id: 2, content: 'Test 2', created_at: '2025-02-17T10:05:00', status: 'read' }
  ]

  beforeEach(() => {
    fetch.mockClear()
    jest.useFakeTimers()
  })

  afterEach(() => {
    jest.useRealTimers()
  })

  describe('Initial Loading', () => {
    it('shows loading indicator initially', () => {
      wrapper = mount(MessagesContainer)
      expect(wrapper.find('.loading').exists()).toBe(true)
    })
  })

  describe('API Interaction', () => {
    it('loads and displays messages successfully', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockMessages)
      })

      wrapper = mount(MessagesContainer)
      await flushPromises()

      expect(wrapper.vm.loading).toBe(false)
      expect(wrapper.findAllComponents({ name: 'MessageItem' })).toHaveLength(2)
      expect(wrapper.find('.loading').exists()).toBe(false)
    })

    it('handles API errors gracefully', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'))
      
      wrapper = mount(MessagesContainer)
      await flushPromises()

      expect(wrapper.vm.loading).toBe(false)
      expect(wrapper.find('.loading').exists()).toBe(false)
    })
  })

  describe('Polling Mechanism', () => {
    it('polls messages every 4 seconds', async () => {
      fetch.mockResolvedValue({ ok: true, json: () => Promise.resolve(mockMessages) })
      
      wrapper = mount(MessagesContainer)
      await flushPromises()
      
      expect(fetch).toHaveBeenCalledTimes(1)
      
      jest.advanceTimersByTime(4000)
      await flushPromises()
      
      expect(fetch).toHaveBeenCalledTimes(2)
    })

    it('stops polling when component is destroyed', async () => {
      fetch.mockResolvedValue({ ok: true, json: () => Promise.resolve(mockMessages) })
      
      wrapper = mount(MessagesContainer)
      await flushPromises()
      
      wrapper.unmount()
      jest.advanceTimersByTime(4000)
      
      expect(fetch).toHaveBeenCalledTimes(1)
    })
  })

  describe('MessageItem Rendering', () => {
    it('passes correct props to MessageItem', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve([mockMessages[0]])
      })

      wrapper = mount(MessagesContainer)
      await flushPromises()

      const messageItem = wrapper.findComponent({ name: 'MessageItem' })
      expect(messageItem.props()).toEqual({
        text: 'Test 1',
        date: '2025-02-17T10:00:00',
        state: 'sent'
      })
    })
  })
})
